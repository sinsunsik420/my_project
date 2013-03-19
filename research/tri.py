# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

from collections import defaultdict as dd
import itertools
import pprint

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

class tri:

    def __init__(self):
        self.tree_data = self.tree()
 
    def tree(self):
        return dd(self.tree)
 
    def insert(self,word):
        for w in word:
            self.tree_data[w].setdefault("score",0.0)
            print self.tree_data
            self.tree_data[w]["score"] += 1.0
            self.tree_data = self.tree_data[w]

    def travalse(self,word):
        result = self.tree_data
        self.search(result,word)

    def search(data,word):
        result = data
        return_word = ""
        for w in word:
            previouse = result
            result = result.get(w)
            if result == None:
                return return_word,previouse
            else:
                return_word += w
                
        return return_word,result

'''
class gya:
    def __init__(self):
        self.data = dd(int)
    def insert(self,word):
        for w in word: 
#            self.data.setdefault(w,0)
            self.data = self.data[w]
            
nga = gya()
nga.insert("hoge")
print nga.data
exit(1)
'''

hoge = tri()
hoge.insert("wbchoge")
print hoge.tree_data
