#! /usr/lib/ruby -Ku
# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

require 'open-uri'
require 'hpricot'
require 'kconv'

sub = open("http://www.yomiuri.co.jp/national/news/20120524-OYT1T01081.htm").read
puts Kconv.guess(sub)

doc = Hpricot(sub) 
(doc/:p).each do |doc|
  puts doc.inner_text
end
