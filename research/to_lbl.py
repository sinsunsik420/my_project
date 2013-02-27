# coding: utf-8

import os,sys
import MeCab
import codecs

#s_urlは語彙の集合、dic_urlは単語の行数(id)を保存

url=open(sys.argv[1])
s_url=set([])
dic_url={}
docu=open(sys.argv[2])

tagger=MeCab.Tagger("-Ochasen")

#chasenにしました

for i,line in enumerate(url):
    s_url.add(line.strip())
    dic_url[line.strip()]=i+1

for line in docu:

    s_line=set([])
    line_data=[]
    node=tagger.parseToNode(line.strip())
    while node:
        s_line.add(node.surface)
        line_data.append(node.surface)
        #     print node.surface
        node=node.next

    s_line.discard('')

#共通集合を抜き出してそれをリスト化。その後、リスト内の単語が記事に何回でてるか数え、dicからidをもらう。

    if len(s_url.intersection(s_line))>0:
        buf=""
        intersect=list(s_url.intersection(s_line))
        for w in intersect:
            buf+=" "+str(dic_url[w])+":"+str(line_data.count(w))
        print buf

