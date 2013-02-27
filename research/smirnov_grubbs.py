# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

import sys
import numpy
from matplotlib import pyplot as plt

def smirnov_grubbs(i,main_data,mean,std,n,t):
    n = float(n)
    test = numpy.fabs((main_data - mean)) / std
    tau = ((n-1.0) * t) / numpy.sqrt(n*(n-2.0) + n*t*t)
    s = str(i)+" is "
    s += "OK" if tau > test else "bags!"
#    print test
    print s

data = numpy.loadtxt(sys.argv[1],delimiter=" ")
a = data[:,0]
n = 100
t = 0.0

while(1):
    t = numpy.fabs(numpy.random.standard_t(n-2))
    if t > 2.5: break 
print t

'''
n,bins,patches = plt.hist(b,100)
plt.savefig("guha_b.png")
plt.clf()
'''
