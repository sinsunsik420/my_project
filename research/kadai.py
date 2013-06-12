# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

import random
from collections import defaultdict as dd
from itertools import combinations
import math
random.seed()
epsilon = 0.00001

def semi_sqrt(a):
    x = 0.0
    x_next = (1.0/a)*9.0

    for i in range(20):
        x = x_next
        x_next = x*(1.5 - 0.5*a*x*x)
        print x_next
    print a*x_next

def rectangle_data(x_min,x_max,y_min,y_max,data):
    return len(filter(lambda x: x_min <= x[0] <= x_max and y_min <= x[1] <= y_max,data))

def r_cost(r,data):
    for A,B in combinations(data,2):
        distance = math.sqrt(math.pow(A[0]-B[0],2)+math.pow(A[1]-B[1],2))
        if distance > r: return False
    return True


if __name__ == '__main__': 
    data = [ (random.randint(-100,100),random.randint(-100,100)) for i in range(100) ]

    max_pair = []
    max_distance = 0
    r1_data = dd(list)
    r2_data = dd(list)

    for A,B in combinations(data,2):
        distance = math.sqrt(math.pow(A[0]-B[0],2)+math.pow(A[1]-B[1],2))
        if max_distance == distance:
            max_pair.append([A,B])
        elif max_distance < distance: 
            max_pair = []
            max_pair.append([A,B])
            max_distance = distance

    print max_pair,max_distance

    max_x = max(data,key=lambda x:x[0])[0]
    min_x = min(data,key=lambda x:x[0])[0]
    min_y = min(data,key=lambda x:x[1])[1]
    
    for x,y in data:
        distance = math.sqrt(math.pow(x-min_x,2)+math.pow(y-min_y,2))
        r1_data[distance].append([x,y])

    for x,y in data:
        distance = math.sqrt(math.pow(x-max_x,2)+math.pow(y-min_y,2))
        r2_data[distance].append([x,y])

    r1_max = max(r1_data.items(),key=lambda x:x[0])
    r1_min = min(r1_data.items(),key=lambda x:x[0])
    
    r2_max = max(r2_data.items(),key=lambda x:x[0])
    r2_min = min(r2_data.items(),key=lambda x:x[0])
    print r1_max,r1_min
    print r2_max,r2_min
