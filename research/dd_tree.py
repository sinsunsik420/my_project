# -*- coding:utf-8 -*-
# -*- encoding:utf-8 -*-

from pprint import pprint
from collections import defaultdict as dd
from itertools import chain

class Tree:

    def __init__(self):
        self.data = self.tree()

    def tree(self): return dd(self.tree)

    def add(self, keys):
        sub = self.data
        for key in keys: sub = sub[key]

    def all_keys(self, sub, text = ""):
        if sub == {}: return text
        else: return [ self.all_keys(sub[k], text + k) for k in sub.keys()] 

    def flatten2(self, L):
        if isinstance(L, list):
            return reduce(lambda a,b: a + self.flatten2(b), L, [])
        else:
            return [L]

    def forward_search(self, string):
        return_str = ""
        sub = self.data
        for s in string:
            if s in sub:
                return_str += s
                sub = sub.get(s)
            else: break

        mach_string = []
        extractions = self.all_keys(sub)
        print extractions
        print self.flatten2(extractions)

if __name__ == "__main__":
    test_tree = Tree()
    train_string = ["hogehoge", "huga", "ngya", "gyahi", "hogehuge","hugehuge","gahogaho","hoogee","hogihogi","hugahuga"]
    for t in train_string: test_tree.add(t)
    test_tree.forward_search("h")
