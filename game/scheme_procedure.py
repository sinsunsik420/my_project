# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

import signal, sys

def evaluater(string):
    cursor = len(string)-1
    ans = 0
    num = ""
    num_stack = []

    while(cursor>=0):
        c = string[cursor]
        if '0' <= c <= '9': num = c + num
        elif c in ['+', '-', '*', '/']:
            ans = process(num_stack, c)
            break
        else:
            if num != "": num_stack.append(int(num))
            num = ""
        cursor-=1

    return ans

def string_process(string):
    cursor = 0
    limit = len(string)
    renew_string = ""

    while(cursor < limit):
        c = string[cursor]
        if c == '(':
            cnt=1
            sub = cursor
            cursor += 1
            while(cnt!=0):
                if string[cursor] == '(': cnt += 1
                if string[cursor] == ')': cnt -= 1
                cursor+=1
            renew_string += " " + str(string_process(string[sub+1:cursor-1])) + " "
        else: renew_string += c

        cursor+=1

    return evaluater(renew_string)

def process(l, pcd):
    if len(l) == 0: exit(200)
    n = l.pop()
    if '+' == pcd:
        while(l!=[]): n += l.pop()
    if '-' == pcd:
        while(l!=[]): n -= l.pop()
    if '*' == pcd:
        while(l!=[]): n *= l.pop()
    if '/' == pcd:
        while(l!=[]): n /= l.pop()
    return n

def signal_handler(signal, frame):
    print("\nBye!!")
    sys.exit(1)

if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    while(1):
        lisp_s = raw_input('>').strip()
        if(lisp_s.count('(') != lisp_s.count(')')): exit(200)
        num = string_process(lisp_s[1:-1])
        print num
