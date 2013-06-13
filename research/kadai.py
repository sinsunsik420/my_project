# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

from argparse import ArgumentParser

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

    import random
    from itertools import combinations
    import math
    random.seed()

    def __init__(self,f,x_min,x_max,y_min,y_max,data_num):
        if not f == "": self.data_file = f
        else:
            self.data_file = ""
            self.x_min = x_min
            self.x_max = x_max
            self.y_min = y_min
            self.num = data_num
        
    def distance(x_1,x_2,y_1,y_2): return math.sqrt((x_1-x_2)*(x_1-x_2)+(y_1-y_2)*(y_1-y_2))

    def kadai_2(self):
        x_range = raw_input("xの範囲を指定してください (例) -1:1")
        x_min,x_max = [int(x) for x in x_range.strip().split(":")]
        y_range = raw_input("xの範囲を指定してください (例) -1:1")
        y_min,y_max = [int(x) for x in x_range.strip().split(":")]

        count = 0
        if self.data_file == "":
            for i in xrange(self.num):
                x = random.randint(self.x_min,self.x_max)
                y = random.randint(self.y_min,self.y_max)
                if x_min <= x <= x_max and y_min <= y <= y_max,data: count += 1
        print("x_min:x_max = %d:%d 及び y_min:y_max = %d:%d の矩形にある点の個数は %d" % (x_min,x_max,y_min,y_max,count) )

    def kadai_3(self):
        cost = raw_input("rを設定してください:")
        cost = float(cost)
        count = raw_input("点の個数を設定してください:")
        count = int(count)
        x_next = random.randint(self.x_min,self.x_max)
        y_next = random.randint(self.y_min,self.y_max)
        if self.data_file == "":
            for i in xrange(self.num):
                x = random.randint(self.x_min,self.x_max)
                y = random.randint(self.y_min,self.y_max)
                if cost < distance(x,x_next,y,y_next):
                    print("到達不可")
                    return 0
                x_next = x
                y_next = y
        print("到達不可")

    def kadai_1(self):
        max_pair1 = []
        min_pair1 = []
        max_pair2 = []
        min_pair2 = []
        
        max_distance1 = 0.0
        min_distance1 = distance(self.x_min,self.x_max,self.y_min,self.y_max)
        max_distance2 = 0.0
        min_distance2 = min_distance1

        if self.data_file == "":
            for i in xrange(self.num):
                x = random.randint(self.x_min,self.x_max)
                y = random.randint(self.y_min,self.y_max)
                distance1 = distance(x,self.x_max,y,self.y_min)
                distance2 = distance(x,self.x_min,y,self.y_min)

                if max_distance1 < distance1: 
                    max_pair1 = []
                    max_pair1.apend((x,y))
                elif max_distance1 == distance1: max_pair1.append((x,y))

                if min_distance1 > distance1: 
                    min_pair1 = []
                    min_pair1.apend((x,y))
                elif min_distance1 == distance1: min_pair1.append((x,y))

                if max_distance2 < distance2: 
                    max_pair2 = []
                    max_pair2.apend((x,y))
                elif max_distance2 == distance2: max_pair2.append((x,y))

                if min_distance2 > distance2: 
                    min_pair2 = []
                    min_pair2.apend((x,y))
                elif min_distance2 == distance2: min_pair2.append((x,y))

                print max_pair1
                print min_pair1
                print max_pair2
                print max_pair2
"""
        else:
            with open(self.data_file) as f:
                for line in f:
                    x,y = [float(x),float(y) for x,y in line.strip().split(" ")]
                    y = random.randint(self.y_min,self.y_max)
                    distance = distance(x - self.x_min,2)+math.pow(y-self.y_min,2))
                    if max_distance < distance: 
                        max_pair = []
                        max_pair.apend((x,y))
                    elif max_distance == distance: max_pair.append((x,y))
                    if min_distance > distance: 
                        min_pair = []
                        min_pair.apend((x,y))
                    elif min_distance == distance: min_pair.append((x,y))
                    
                    print max_pair
                    print min_pair
"""


if __name__ == '__main__':
    args = getargs()
    x_min,x_max = [ int(x) for x in args.x_max_min..strip().split(":")]
    y_min,y_max = [ int(x) for x in args.y_max_min..strip().split(":")]
    k = Kadai.new(args.data_file,args.num,x_min,x_max,y_min,y_max)
    for kadai in args.kadai:
        if kadai == '1': k.kadai_1()
        elif kadai == '2': k.kadai_2()
        else: n = k.kadai_3()


"""
epsilon = 0.00001

def semi_sqrt(a):
    x = 0.0
    x_next = (1.0/a)*9.0

    for i in range(20):
        x = x_next
        x_next = x*(1.5 - 0.5*a*x*x)
        print x_next
    print a*x_next
"""
