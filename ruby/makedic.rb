#!/usr/bin/ruby
# -*- coding: utf-8 -*-

require 'kconv'

if $*[0] =~ /wiki/ then
  origin = "wikipedia_keyword"
elsif $*[0] =~ /furigana/ then
  origin = "hatena_keyword"
else
  origin = "unknown"
end

open($*[0]).each do |line|
  if origin == "hatena_keyword" then
    title = line.split("\t")[1].strip.toutf8
  else
    title = line.strip
  end
  
  next if title =~ /^\./
  next if title =~ /,/
  next if title =~ /[0-9]{4}/
  next if title =~ /^[-.0-9]+$/
  
  score = [-32768.0, (6000 - 200 *(title.size**1.3))].max.to_i
  
  if title.size > 9 then
    out = "#{title},-1,-1,#{score},名詞,一般,*,*,*,*,#{title},*,*,#{origin},\n"
    print out.toutf8
  end
end
