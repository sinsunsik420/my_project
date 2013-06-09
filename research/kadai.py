# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

import random
from itertools import combinations
import math
random.seed()

data = [ (random.randint(0,100),random.randint(0,100)) for i in range(100) ]
max_pair = []
max_distance = 0

for A,B in combinations(data,2):
    distance = math.sqrt(math.pow(A[0]-B[0],2)+math.pow(A[1]-B[1],2))
    if max_distance < distance: 
        max_pair = [A,B]
        max_distance = distance
print max_pair,max_distance

x_min = 10
x_max = 60
y_min = 44
y_max = 89

select_data = filter(lambda x: x_min <= x[0] <= x_max and y_min <= x[1] <= y_max,data)
print len(select_data)

#rand_i = random.randint(0,50)
#rand_j = random.randint(50,100)
r = 50
flag = "True"
for A,B in combinations(data[5:10],2):
    distance = math.sqrt(math.pow(A[0]-B[0],2)+math.pow(A[1]-B[1],2))
    if distance > r:
        flag = "False"
        break

print flag
