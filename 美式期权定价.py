# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 20:45:59 2019

@author: Xiaodong, Chen
"""

class AmericanOption:
    """ 求解美式期权的期初价值 """
    
    def __init__(self, up, down, free_risk, steps, init_price, strike, type_):
        """ 股票二叉树框架 : 0 < d < 1 + r < u """
        assert 0 < down < 1 + free_risk < up
        self.u = up
        self.d = down
        self.r = free_risk
        self.N = steps
        self.s0 = init_price
        self.K = strike
        self.type_ = type_
        self.p = (1 + free_risk - down) / (up - down)
        self.q = (up - 1 - free_risk) / (up - down)
    
    @staticmethod
    def execise_payoff(s, K, type_):
        """ 立即行权收益 """
        if type_ == 'call':
            return s - K
        if type_ == 'put':
            return K - s
        
    def get_step_value(self, n, s):
        """ n是递推下标，s是股价，注意期权支付是股价的函数 
         Page10 V的递推公式优化 """
        if n == self.N:
            return max(0, AmericanOption.execise_payoff(s, self.K, self.type_))
        else:
            us = self.u * s
            ds = self.d * s
            return max(AmericanOption.execise_payoff(s, self.K, self.type_),
                       (self.p * self.get_step_value(n + 1, us) + \
                        self.q * self.get_step_value(n + 1, ds)) / (1 + self.r)
                       )
        
    @property
    def init_value(self):
        return self.get_step_value(0, self.s0)

# ================= Example :   Page 81 例4.2.1看跌期权   =====================
u = 2; d = 0.5; r = 0.25; steps = 2; s0 = 4; K = 5;
put = AmericanOption(u, d, r, steps, s0, K, 'put')
print(put.init_value)