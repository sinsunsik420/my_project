# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

import sys,json,re
from math import * 
import pprint
from collections import defaultdict as dd 
#import numpy

class tail_recursive(object):

    def __init__(self, func):
        self.func = func
        self.firstcall = True
        self.CONTINUE = object()

    def __call__(self, *args, **kwd):
        if self.firstcall:
            func = self.func
            CONTINUE = self.CONTINUE
            self.firstcall = False
            try:
                while True:
                    result = func(*args, **kwd)
                    if result is CONTINUE: # update arguments
                        args, kwd = self.argskwd
                    else: # last call
                        return result
            finally:
                self.firstcall = True
        else: # return the arguments of the tail call
            self.argskwd = args, kwd
            return self.CONTINUE

def make_matrix(matrix,activity,cls):
    for action in activity:
        matrix[action].setdefault("0_data",0.0)
        matrix[action].setdefault("1_data",0.0)
        if cls == "0":
            matrix[action]["0_data"] += 1.0
        else:
            matrix[action]["1_data"] += 1.0

def node_insert(forest,activity,cls):
    for node in activity:
        forest[action].setdefault("0_data",0.0)
        forest[action].setdefault("1_data",0.0)
        if cls == "0":
            matrix[action]["0_data"] += 1.0
        else:
            matrix[action]["1_data"] += 1.0
        forest = forest[action]

def dump_forest(f_name,forest):
    open(f_name,"w").write(json.dumps(forest))

def tree():
    return dd(tree)

def make_tree_matrix(forest,matrix,main_en):
    for action,v in matrix.items(): 
        e = entropy(v.values())
        matrix[action]["gain"] = main_en - e
    top = sorted(matrix.items(),key=lambda x:x[1]["gain"],reverse=True)[:100]
    print sorted(top,key=lambda x:x[1]["0_data"],reverse=True)
        
def search(forest,activity):
    result = forest
    while(1):
        action = activity.pop(0)
        previouse = result
        result = result.get(action)
        if result == None: 
            return previouse['0_data'],previouse['1_data']

def entropy(v):
#    print v
    m,n = v[0],v[1]
    all_data = m + n
    if n == 0.0 or m == 0.0: return 0.0
    return (m/all_data)*log(all_data/m) + (n/all_data)*log(all_data/n)

if __name__ == "__main__":
    flag = re.compile(">")
    user_id = ""
    cls = ""
    matrix = dd(lambda:dd(float))
    forest = tree()
    yes_data = 0.0
    no_data = 0.0

    for i,line in enumerate(open(sys.argv[1]).readlines()[:100000]):
        #    print i
        if flag.match(line):
            if not i == 0: make_matrix(matrix,activity,cls)
            user_id,cls = line[1:].strip().split("\t")
            if cls == "0": yes_data += 1.0
            else: no_data += 1.0
            activity = []
        else:
            t,action = line.strip().split("\t")
            activity.append(action)
            
#dump_forest("decision.json",forest)
    main_en = entropy([yes_data,no_data])
    make_tree_matrix(forest,matrix,main_en)
            
    for i,line in enumerate(open(sys.argv[2]).readlines()[:10000]):
        #    print i
        if flag.match(line):
#            if not i == 0: print search(forest,activity)
            activity = []
        else:
            t,action = line.strip().split("\t")
            activity.append(action)
            
