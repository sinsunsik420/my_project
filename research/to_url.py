#coding:utf-8
import MeCab
import sys
import codecs
import optparse

def args():
    parser=optparse.OptionParser()
    parser.add_option("-f",dest="filename",help="text_data")
    parser.add_option("--line",dest="txt_ac",type="int",help="0:all_text_data\n 1:first_line_data in texts",default=0)

    (options,args)=parser.parse_args()
    return (options,args)
(options,args)=args()

file=options.filename
data=open(file)

#print data.readlines()[0].split("。")[0]
#exit()

tagger = MeCab.Tagger("-Ochasen")
word=set([])

for line in data :
    if options.txt_ac==1:
        node = tagger.parseToNode(line.split("。")[0])
    else:
        node = tagger.parseToNode(line)
        
    while node:
        hinsi=node.feature.find('名詞')
        if hinsi==0 and len(node.surface)>3 :
            word.add(node.surface)
        node = node.next
#    print(i+1,"\n")

#word=list(word).sort()
for w in word:
    print '%s' % (w)
