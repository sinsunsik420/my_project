require 'open-uri'
require 'mechanize'

id = ARGV[0]
id = id.match(/sm\d*/)
puts id

mail = "sinsunsik420@gmail.com"
pass = "azumanga"
agent = Mechanize.new
agent.post("https://secure.nicovideo.jp/secure/login?site=niconico","mail"=>mail,"password"=>pass)
agent.get("http://www.nicovideo.jp/watch/#{id}")

moviedata = agent.get("http://flapi.nicovideo.jp/api/getflv/#{id}")
movie_url = moviedata.body.match(/http.*low/)
movie_url = URI.unescape(movie_url.to_s)

open("test.mp4", "wb") do |output|
  output.print agent.get_file(movie_url)
end
