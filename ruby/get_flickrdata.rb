# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

#分散化、モジュール化、スレッドの自動生成＋パラメータ管理 現在進行形
require "active_support/core_ext/hash"
require "flickraw"
require "json"
require "redis"
require "time"
require "pp"

#Flickr_API_key

FlickRaw.api_key = "8ae3ebe635df0ac6c03d31ba7009c3ee"
FlickRaw.shared_secret = "100d3e6f82e85f7c"
FlickRaw.proxy = "http://cache.st.ryukoku.ac.jp:8080/"

class Get_flickr

  def initialize
    @locker = Mutex.new
    @owners = Queue.new
    @pool = []
  end

  def daytime
    return_str = ""
    d = Time.now
    return_str += d.year.to_s+"_"+d.month.to_s+"_"+d.day.to_s
    return return_str
  end

  #server_adaptor.Redisへの書き込みはここだけで行う。
  def save_redis
    redis = Redis.new
    f_name = "redis_save_log"+daytime
    log_file = open(f_name,"a") 
    while(1) do
      #queueが空の時、ちょっと待ってみる
      sleep(60) if @pool == []
      #main_threadのみならexit
      break if Thread.list.size == 1
      @pool.each{|data| 
          next if redis.exists data[0]
          redis.hset data[0],data[1],data[2]
          log_file.puts data[0]+" "+data[1]+"_data dumped",Time.now
        }
      redis.save
      sleep(60)
    end
    log_file.puts "dump_data finished",Time.now
    log_file.close
  end
  
#threadのアクションのまとめ。serverアダプタは別の関数で管理
  def thread_action(thread_num)
    
    f_name = "thread_log"+daytime
    while(1) do
      break if @owners.empty?
      user = ""
      @locker.synchronize{ user = @owners.pop }

      dump_data,messages = get_fav(user)
      @locker.synchronize{
        log_file = open(f_name,"a") 

        #error発生時のログファイルへの書出し。dumpが無いときもログに書き出す。
        if dump_data == [] then
          if messages == "" then
            log_file.puts "thread:"+thread_num+" "+user+" does not have fav_list",Time.now
          else
            log_file.puts "thread:"+thread_num,messages,Time.now
          end
        else
          @pool.push([user,"favorites_list",dump_data])
          log_file.puts "thread:"+thread_num+" writed "+user+" fav_list",Time.now
        end
        log_file.close
      }
      
      dump_data,messages = get_friend(user)
      @locker.synchronize{
        log_file = open(f_name,"a")
        if dump_data == [] then
          if messages == "" then
            log_file.puts "thread:"+thread_num+" "+user+" does not have friend_list",Time.now
          else
            log_file.puts "thread:"+thread_num,messages,Time.now
          end
        else
          @pool.push([user,"friend_list",dump_data])
          log_file.puts "thread:"+thread_num+" writed "+user+" friend_list",Time.now
        end
        log_file.close
      }
      
    end
    @locker.synchronize{
      log_file = open(f_name,"a") 
      log_file.puts "thread:"+thread_num+"_data finished",Time.now
      log_file.close
    }
  end  
  
#fav_dataを収集。タグ情報をメインに収集
  def get_fav(user)
    
    return_data = []
#必要なアイテム => "owner","tags","title","date_faved","nsid","username"
#    need_data = ["owner","tags","title","date_faved","nsid","username"]

#タイムアウトは別に扱う。他のエラーには未対応    
    begin
      favolists = flickr.favorites.getPublicList(:user_id=>user,:extras=>"tags")
      sleep(5)
    rescue Timeout::Error => ex
      puts ex.class
      sleep(30)
    rescue => ex
      return [],ex.class
    end
    return [],user+" is not friends" if favolists.total == 0

    pages = favolists.pages    
    pages.times{|i|
      favolists.each{|d|
        h = d.to_hash
        h.slice!(:owner,:tags,:title,:date_faved,:nsid,:username)
        return_data.push(h)
      }
      if pages > i+1 then 
        begin
          favolists = flickr.favorites.getPublicList(:user_id=>user,:extras=>"tags",:page=>i+2)
          sleep(5)
        rescue Timeout::Error => ex
          puts ex.class
          sleep(30)
        rescue => ex
          return [],ex.class
        end
      end
    }
    return return_data.to_json,""  
  end
  
#friend_dataを収集
  def get_friend(user)
    
    return_data = []
#必要なアイテム
#    need_data = ["owner","tags","title","date_faved","nsid","username"]
    
#タイムアウトは別に扱う。他のエラーには未対応
    begin
      friends = flickr.contacts.getPublicList(:user_id=>user)
      sleep(5)
    rescue Timeout::Error => ex
      puts ex.class
      sleep(30)
    rescue => ex 
      return [],ex.class
    end
    return [],user+" is not friends" if friends.total == 0

#ページ数。最大イテレート数
    pages = friends.pages
#必要なアイテム以外削除    
    pages.times{|i|
      friends.each{|d|
        h = d.to_hash
        h.slice!(:owner,:tags,:title,:date_faved,:nsid,:username)
        return_data.push(h)
      }
      if pages > i+1 then 
        begin
          friends = flickr.contacts.getPublicList(:user_id=>user,:page=>i+2)
          sleep(5)
        rescue Timeout::Error => ex
          puts ex.class
          sleep(30)
        rescue => ex
          return [],ex.class
        end
      end
    }
    return return_data.to_json,""    
  end

#スレッド共有のQueue
  attr_writer :owners
end

#main関数
if __FILE__ == $0

  while(1) do
    
    #activeなRecent_userのみ収集
    list = flickr.photos.getRecent
    action = Get_flickr.new
    action.owners = list.map{|v| v["owner"]}
    sleep(5)
    
    t1 = Thread.new do
      Thread.pass
      action.thread_action("1")
    end
    
    sleep(10)
    
    t2 = Thread.new do
      Thread.pass
      action.thread_action("2")
    end
    
    sleep(30)
    action.save_redis
    
    t1.join
    t2.join 
    
  end
end
