# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 22:32:33 2019

@author: Xiaodong, Chen
"""

class EuropeanOption:
    """ 求解欧式期权的期初价值 """
    
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
    
    def get_step_value(self, n, s):
        """ n是递推下标，s是股价，注意期权支付是股价的函数 
         Page10 V的递推公式优化 """
        if n == self.N:
            if self.type_ == 'call':
                return max(0, s - self.K)
            if self.type_ == 'put':
                return max(0, self.K - s)
        else:
            us = self.u * s
            ds = self.d * s
            return (self.p * self.get_step_value(n + 1, us) + \
                    self.q * self.get_step_value(n + 1, ds)) / (1 + self.r)
        
    @property
    def init_value(self):
        return self.get_step_value(0, self.s0)


# ================= Example 1:   Page 3 例1.1.1看涨期权   =====================
u = 2; d = 0.5; r = 0.25; steps = 1; s0 = 4; K = 5;
call = EuropeanOption(u, d, r, steps, s0, K, 'call')
print(call.init_value)

# ====================== Example 2: Page 13 例1.3.1看跌期权  ==================
u = 2; d = 0.5; r = 0.25; steps = 3; s0 = 4; K = 5;
put = EuropeanOption(u, d, r, steps, s0, K, 'put')
print(put.init_value)

# ================= Example 3:   Page 18 习题1.3   =====================
u = 2; d = 0.5; r = 0.25; steps = 1; s0 = 4; K = 0;
call = EuropeanOption(u, d, r, steps, s0, K, 'call')
print(call.init_value)    # 显然就是s0