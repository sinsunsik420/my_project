# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

from argparse import ArgumentParser
from multiprocessing import Pool,Value,Array
from random import randint
from math import sqrt
from ctypes import Structure,c_int

def tomap(args): return getattr(args[0], args[1])(*args[2:])

def toapply(cls, mtd_name, *args, **kwargs): return getattr(cls, mtd_name)(*args, **kwargs)

class MulHelper(object):
    def __init__(self, cls, mtd_name):
        self.cls = cls
        self.mtd_name = mtd_name

    def __call__(self, *args, **kwargs): return getattr(self.cls, self.mtd_name)(*args, **kwargs)

class Point(Structure):
    _fields_ = [('i', c_int), ('i', c_int)]

def getargs():

    parser = ArgumentParser(description='It is the kadai program.')
    parser.add_argument('-f', dest='data_file', help='data file path.')
    parser.add_argument('-n', dest='num', help='number of points.', default=100,type=int)
    parser.add_argument('--x_min_max', dest='x_min_max', help='for example, --x_min_max -10:100.',default="-100:100")
    parser.add_argument('--y_min_max', dest='y_min_max', help='for example, --y_min_max -10:100.',default="-100:100")
    parser.add_argument('--kadai', dest='kadai', help='for example, you need kadai 1 and 2 results, set arguments such, --kadai 12.',default='1')
    parser.add_argument('--ncore', dest='ncore', help='if you want to multiprocessing, set num of core.',default=1,type=int)

    return parser.parse_args()

class Kadai:

    def __init__(self,o_f,x_min,x_max,y_min,y_max,data_num,ncore):
        self.f = o_f
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.num = data_num
        self.ncore = ncore
        self.data = []

    def thread_wrapper(self,args): return args[0](*args[1:])

    def generate_data(self):
        pool = Pool(self.ncore)
        if self.f == None:
            self.data = pool.map(MulHelper(self,'random_data_gene'),range(self.num))
        else:
            with open(self.f) as f:
                self.data = pool.map( MulHelper(self,'thread_wrapper'),[ (MulHelper(self,'file_process'),line) for line in f ] )

    def random_data_gene(self,x): return (randint(self.x_min,self.x_max), randint(self.y_min,self.y_max))

    def max_min_distance1(self,p): return self.distance(p[0],self.x_max,p[1],self.y_min)

    def max_min_distance2(self,p): return self.distance(p[0],self.x_min,p[1],self.y_min)

    def file_process(self,line):
        x,y = line.strip().split(" ")
        x = int(x)
        y = int(y)

        if self.x_max < x: self.x_max = x
        elif self.x_min > x: self.x_min = x

        if self.y_max < y: self.y_max = y
        elif self.y_min > y: self.y_min = y

        return (x,y)
    
    def count_filter(self,data,x_min,x_max,y_min,y_max): return (x_min <= data[0] <= x_max and y_min <= data[1] <= y_max) 

    def reach_out(self,p1,p2,cost):
        distance = self.distance(*(p1+p2))
        return True if distance < cost else False

    def distance(self,x_1,x_2,y_1,y_2): return sqrt((x_1-x_2)*(x_1-x_2)+(y_1-y_2)*(y_1-y_2))

    def kadai_1(self):
        pool = Pool(self.ncore)
        result = pool.map(MulHelper(self,'max_min_distance1'),[d for d in self.data])
        max_data1 = max(enumerate(result),key=lambda x:x[1])
        max_point1 = self.data[max_data1[0]]
        min_data1 = min(enumerate(result),key=lambda x:x[1])                   
        min_point1 = self.data[min_data1[0]]
        distance1 = self.distance(max_point1[0],min_point1[0],max_point1[1],min_point1[1])

        result = pool.map(MulHelper(self,'max_min_distance2'),[d for d in self.data])
        max_data2 = max(enumerate(result),key=lambda x:x[1])                   
        max_point2 = self.data[max_data2[0]]
        min_data2 = min(enumerate(result),key=lambda x:x[1])                   
        min_point2 = self.data[min_data2[0]]
        distance2 = self.distance(max_point2[0],min_point2[0],max_point2[1],min_point2[1])

        min_data = (max_point1,min_point1,distance1) if  distance1 < distance2 else (max_point2,min_point2,distance2)
        print("距離の最大値は%s,ペアは(x1,y1)=(%s,%s),(x2,y2)=(%s,%s)" % ( str(max_data[2]),str(max_data[0][0]),str(max_data[0][1]),str(max_data[1][0]),str(max_data[1][1]) ))

    def kadai_2(self):
        x_range = raw_input("xの範囲を指定してください (例) -1:1\n")
        x_min,x_max = [int(x) for x in x_range.strip().split(":")]
        y_range = raw_input("yの範囲を指定してください (例) -1:1\n")
        y_min,y_max = [int(y) for y in y_range.strip().split(":")]
        pool = Pool(self.ncore)
        count = sum(pool.map(MulHelper(self,'thread_wrapper'),[(MulHelper(self,'count_filter'), d, x_min, x_max, y_min, y_max) for d in self.data]))
        print("x_min:x_max = %s:%s 及び y_min:y_max = %s:%s の矩形にある点の個数は %d" % ( str(x_min), str(x_max), str(y_min), str(y_max), count ))

    def kadai_3(self):
        cost = raw_input("rを設定してください: ")
        cost = float(cost)
        p_q = raw_input("pとqを設定してください: (例)1:10 ただし p,q > 0\n")
        p,q = [int(x) for x in p_q.strip().split(":")]
        pool = Pool(self.ncore)
        ex_data = self.data[p:q]
        gyo = [ (MulHelper(self,'reach_out'), p1, p2, cost) for p1,p2 in zip(ex_data[1:],ex_data[:-1]) ]
        print(False) if False in pool.map( MulHelper(self,'thread_wrapper'),[ (MulHelper(self,'reach_out'), p1, p2, cost) for p1,p2 in zip(self.data[1:],self.data[:-1]) ] ) else True

if __name__ == '__main__':

    args = getargs()
    x_min,x_max = [ int(x) for x in args.x_min_max.strip().split(":")]
    y_min,y_max = [ int(x) for x in args.y_min_max.strip().split(":")]
    k = Kadai(args.data_file,x_min,x_max,y_min,y_max,args.num,args.ncore)
    k.generate_data()
    for kadai in args.kadai:
        if kadai == '1': k.kadai_1()
        elif kadai == '2': k.kadai_2()
        else: n = k.kadai_3()
