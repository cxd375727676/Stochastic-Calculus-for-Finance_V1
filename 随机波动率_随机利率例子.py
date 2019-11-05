# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:11:28 2019

@author: Xiaodong, Chen

Page 20 习题1.9
"""

p = q = 0.5
r = 0
N = 5
K = 80
s0 = 80
def get_value(n, s):
    if n == N:
        return max(0, s - K)
    else:
        return (p * get_value(n + 1, s + 10) + q * get_value(n + 1, s - 10)) / (1 + r)


print(get_value(0, s0))                