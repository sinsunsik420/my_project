# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

import math
import generate_testdata
import random

def g(x): return x*math.exp(-x*x*0.5)

def distance(p1,p2): return sum([(d1-d2)*(d1-d2) for d1, d2 in zip(p1, p2)])
#thleshold + labeling via data
def mean_shift(data):
    n = len(data)
    h = 100.0
    hd = 100.0*100.0
    while(data != []):
        sample = random.sample(data,1)[0]
        neighbors = filter(lambda x: distance(x,sample) < h, data)
        if neibors != 0: 
            print sample
            continue
        fraq_child = [0.0,0.0]
        fraq_mother = 0.0
        print len(data)
        for neighbor in neighbors:
            g_value = g(distance(sample,neighbor)/hd)
            fraq_mother += g_value
            fraq_child =  map((lambda x,y:x+y*g_value),fraq_child, neighbor)

        sample = map((lambda x:x/fraq_mother), fraq_child)
        print sample
        for n in neighbors: data.remove(n)

if __name__ == '__main__':
    data = generate_testdata.sample_data(10,2)
    mean_shift(data)
