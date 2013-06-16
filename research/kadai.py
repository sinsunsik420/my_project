# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

from argparse import ArgumentParser
from multiprocessing import Pool,Value,Array
from random import randint
from math import sqrt
from ctypes import Structure,c_int
from itertools import product,combinations

#クラス内でマルチプロセスを行うためのヘルパー関数。
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
    parser.add_argument('-n', dest='num', help='the number of test points. if you send data file, this option dose not work.', default=100,type=int)
    parser.add_argument('--x_min_max', dest='x_min_max', help='the xrange for test data. for example, --x_min_max -10:100.',default="-100:100")
    parser.add_argument('--y_min_max', dest='y_min_max', help='the yrange for test data. for example, --y_min_max -10:100.',default="-100:100")
    parser.add_argument('--kadai', dest='kadai', help='set kadai number. for example, you need kadai 1 and 2 results, set arguments --kadai 12.',default='1')
    parser.add_argument('--ncore', dest='ncore', help='if you want to multiprocess, set int argument.',default=1,type=int)

    return parser.parse_args()

#生まれて2回目のクラス
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

#マルチスレッドに複数引数で処理を行うためのラッパー
    def thread_wrapper(self,args): return args[0](*args[1:])

#ファイルが与えられるか否かで、データの生成を分岐
    def generate_data(self):
        pool = Pool(self.ncore)
        if self.f == None:
            self.data = pool.map(MulHelper(self,'random_data_gene'),range(self.num))
        else:
            with open(self.f) as f:
                self.data = pool.map(MulHelper(self,'file_process'),[ line for line in f ])

#テストデータの生成関数
    def random_data_gene(self,x): return (randint(self.x_min,self.x_max), randint(self.y_min,self.y_max))

#課題1で利用。隣り合うx値上に並ぶ点のリストがsetである。
#初めに、set内の点で距離を求め、次にset同士で距離の計算を行う。
#最終的に、一番低い値のdistanceを返す。なお、set内のデータは降順にソート済みである。
    def search_min(self,set1,set2):
        min_distance = 1000000.0
        if len(set1)>1:
            for p1,p2 in zip(set1[1:],set1[:-1]):
                d = self.distance(p1[0],p2[0],p1[1],p2[1]) 
                if min_distance > d: min_distance = d

        if len(set2)>1:
            for p1,p2 in zip(set2[1:],set2[:-1]):
                d = self.distance(p1[0],p2[0],p1[1],p2[1]) 
                if min_distance > d: min_distancxe = d

        for p1,p2 in product(set1,set2):
            d = self.distance(p1[0],p2[0],p1[1],p2[1]) 
            if min_distance > d: min_distance = d

        return min_distance

# -f でファイルが与えられた時に行われる処理
    def file_process(self,line):
        data = line.strip().split(" ")
        x = float(data[0])
        y = float(data[1])
        return (x,y)
    
#課題2にて利用。矩形に含まれればTrueを返す。
    def count_filter(self,data,x_min,x_max,y_min,y_max): return (x_min <= data[0] <= x_max and y_min <= data[1] <= y_max) 

#課題3にて利用。distance < rならTrueを返す。
    def reach_out(self,p1,p2,cost):
        distance = self.distance(*(p1+p2))
        return True if distance < cost else False

    def distance(self,x_1,x_2,y_1,y_2): return sqrt((x_1-x_2)*(x_1-x_2)+(y_1-y_2)*(y_1-y_2))

#課題1の処理
    def kadai_1(self):
        pool = Pool(self.ncore)
        x_colmns = list(set([x[0] for x in self.data]))
        x_colmns.sort()
        s_data = [sorted(filter(lambda x: x[0] == c,self.data),key=lambda x:x[1],reverse=False) for c in x_colmns ]
        result = pool.map(MulHelper(self,'thread_wrapper'),[ (MulHelper(self,'search_min'),set1,set2) for set1,set2 in zip(s_data[1:],s_data[:-1]) ])
        return min(result)
#課題2の処理   
    def kadai_2(self):
        x_range = raw_input("xの範囲を指定してください (例) -1:1\n")
        x_min,x_max = [int(x) for x in x_range.strip().split(":")]
        y_range = raw_input("yの範囲を指定してください (例) -1:1\n")
        y_min,y_max = [int(y) for y in y_range.strip().split(":")]
        pool = Pool(self.ncore)
        count = sum(pool.map(MulHelper(self,'thread_wrapper'),[(MulHelper(self,'count_filter'), d, x_min, x_max, y_min, y_max) for d in self.data]))

#課題3の処理
    def kadai_3(self):
        cost = raw_input("rを設定してください: ")
        cost = float(cost)
        p_q = raw_input("pとqを設定してください: (例)1:10 ただし p,q > 0\n")
        p,q = [int(x) for x in p_q.strip().split(":")]
        pool = Pool(self.ncore)
        ex_data = self.data[p:q]
        gyo = [ (MulHelper(self,'reach_out'), p1, p2, cost) for p1,p2 in zip(ex_data[1:],ex_data[:-1]) ]
        return False if False in pool.map( MulHelper(self,'thread_wrapper'),[ (MulHelper(self,'reach_out'), p1, p2, cost) for p1,p2 in zip(self.data[1:],self.data[:-1]) ] ) else True

if __name__ == '__main__':

    args = getargs()
    x_min,x_max = [ int(x) for x in args.x_min_max.strip().split(":")]
    y_min,y_max = [ int(x) for x in args.y_min_max.strip().split(":")]
    k = Kadai(args.data_file,x_min,x_max,y_min,y_max,args.num,args.ncore)
    k.generate_data()
    for kadai in args.kadai:
        if kadai == '1':
            result = k.kadai_1()
            print("距離の最小値は%s" % result )
        elif kadai == '2': 
            result = k.kadai_2()
            print("矩形の中にある点の個数は %d" % count )
        else:
            result = k.kadai_3()
            print("到達可") if result else "到達不可"
