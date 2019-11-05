# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 00:02:11 2019

@author: Xiaodong, Chen
"""

class EuropeanLookBackOption:
    """ 求解欧式回望期权的期初价值, 算法优化 """
    
    def __init__(self, up, down, free_risk, steps, 
                 init_price, type_1, type_2, strike=None):
        """ 股票二叉树框架 : 0 < d < 1 + r < u 
        type_1: 'fix' or 'float'
        type_2: 'call' or 'put'
        """
        assert 0 < down < 1 + free_risk < up
        self.u = up
        self.d = down
        self.r = free_risk
        self.N = steps
        self.s0 = init_price
        self.type_1 = type_1
        self.type_2 = type_2
        self.p = (1 + free_risk - down) / (up - down)
        self.q = (up - 1 - free_risk) / (up - down)       
        if type_1 == 'fix':
            self.K = strike
    
    def get_step_value(self, n, s, m):
        """ n是递推下标，s是股价，m是最大值或最小值，
        注意期权支付是股价，最大（小）值的函数 
         Page10 V的递推公式优化 """
        if n == self.N:
            if self.type_1 == 'fix' and self.type_2 == 'call':
                return max(0, m - self.K)
            if self.type_1 == 'fix' and self.type_2 == 'put':
                return max(0, self.K - m)
            if self.type_1 == 'float' and self.type_2 == 'call':
                return s - m
            if self.type_1 == 'float' and self.type_2 == 'put':
                return m - s
        else:
            us = self.u * s
            ds = self.d * s
            if (self.type_1 == 'fix' and self.type_2 == 'call') or \
            (self.type_1 == 'float' and self.type_2 == 'put'):
                return (self.p * self.get_step_value(n + 1, us, max(m, us)) + \
                        self.q * self.get_step_value(n + 1, ds, m)) / (1 + self.r)
            if (self.type_1 == 'fix' and self.type_2 == 'put') or \
            (self.type_1 == 'float' and self.type_2 == 'call'):
                return (self.p * self.get_step_value(n + 1, us, m) + \
                        self.q * self.get_step_value(n + 1, ds, min(m, ds))
                        ) / (1 + self.r)
                        
    @property
    def init_value(self):
        return self.get_step_value(0, self.s0, self.s0)

# ====================== Example : Page 12 例1.2.4回望期权  ==================
u = 2; d = 0.5; r = 0.25; steps = 3; s0 = 4;
float_put = EuropeanLookBackOption(u, d, r, steps, s0, 'float', 'put')
print(float_put.init_value)