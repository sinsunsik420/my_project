#coding:utf-8
import MeCab
import sys
import codecs
import optparse

def args():
    parser=optparse.OptionParser()
    parser.add_option("-f",dest="filename",help="text_data")
    parser.add_option("--ourl",dest="urlfile",help="output_url_data_")
    parser.add_option("--olbl",dest="lblfile",help="output_lbl_data")

    (options,args)=parser.parse_args()
    return (options,args)

(options,args)=args()
data=open(options.filename,'r')
#data=codecs.open(options.filename,'r','utf-8')
ourl=codecs.open(options.urlfile,"w",'utf-8')
olbl=codecs.open(options.lblfile,"w",'utf-8')

#print data.readlines()[0].split("。")[0]
#exit()

tagger = MeCab.Tagger("-Ochasen")
word=set([])

txt_data=[]

for line in data:
    subdata=""
    node = tagger.parseToNode(line)

    while node:
        hinsi=node.feature.find('名詞')
        if hinsi==0 and len(node.surface)>3 :
            word.add(node.surface)
            subdata += " " + node.surface
        node = node.next
    txt_data.append(subdata)

#word=list(word).sort()
l_word=list(word)
for w in word:
    ourl.write(w.decode('utf-8') + "\n")

ourl.close

for line in txt_data:

#共通集合を抜き出してそれをリスト化。その後、リスト内の単語が記事に何回でてるか数え、dicからidをもらう。

    s_line_words=set([])
    buf=""
    lines=line.split(' ')
    lines.remove("")
    if len(lines)>0:
 #       print lines
        [s_line_words.add(w) for w in lines]
        inter_words=word.intersection(s_line_words)
        for data in s_line_words:
            buf+=" "+str(l_word.index(data)+1)+":"+str(lines.count(data))
        olbl.write(buf+"\n")
            
