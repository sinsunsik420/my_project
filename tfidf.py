# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys
import random
import codecs
import optparse
import math

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

def args():
    parser = optparse.OptionParser()
    parser.add_option("--furl",dest="urlfile",help="url_file")
    parser.add_option("--flbl",dest="lblfile",help="lbl_file")
    
    (options,args)=parser.parse_args()
    return (options,args)

def tf(data,tf_data):
    tf = 0.0
    for i,d in enumerate(data):
        for id,freq in d.items():
            tf = freq / float(sum(d.values()))
            tf_data[i][id] = tf
#            print tf

def idf(data,idf_data,voca_size):
    idf = 0.0
    i = 0
    all_docs = float(len(data))
    while i<voca_size:
        freq = 0
        for d in data:
            if d.has_key(i+1):
                freq += 1
        idf_data.append(math.log(all_docs/float(freq))) 
        i += 1
#    print idf_data

def tfidf(tf,idf,word):
    for i,v in enumerate(tf):
        print i+1
        for id,value in v.items():
            print "\t%s:%lf"  % (word[id-1],value*idf[id-1])

if __name__ == '__main__':

    (options,args) = args()

    file_url = [w.strip() for w in codecs.open(options.urlfile,'r',"utf-8").readlines()]
    file_lbl = [w.strip() for w in open(options.lblfile).readlines()]
#    all_docs = float(len(file_lbl))
    lbl_data = [{} for i in range(len(file_lbl))]
    tf_data = [{} for i in range(len(file_lbl))]
    idf_data = []
#    print lbl_data
#    exit(1)
#    print all_docs
    

    for i, doc in enumerate(file_lbl):
        
        term_id_and_freq = doc.split(" ")
        for id_and_freq in term_id_and_freq:
            data = id_and_freq.split(":")
            lbl_data[i][int(data[0])]=int(data[1])
#        print lbl_data
    tf(lbl_data,tf_data)
#    print tf_data
    idf(lbl_data,idf_data,len(file_url))
    
    tfidf(tf_data,idf_data,file_url)
