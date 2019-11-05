# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:58:17 2019

@author: Xiaodong, Chen
"""

class EuropeanDerivative:
    """ 求解欧式一般衍生证券的期初价值 """
    
    def __init__(self, up, down, free_risk, steps, last_payfunc):
        """ 股票二叉树框架 : 0 < d < 1 + r < u """
        assert 0 < down < 1 + free_risk < up
        self.u = up
        self.d = down
        self.r = free_risk
        self.N = steps
        self.last_payfunc = last_payfunc
        self.p = (1 + free_risk - down) / (up - down)
        self.q = (up - 1 - free_risk) / (up - down)
    
    def get_step_value(self, *process):
        """ 各路径下的衍生品价值
        比如 get_step_value(0,1,1) 表示已知股票下跌上涨上涨时衍生品价值 
        见 Page10 V的递推公式 """
        if len(process) == self.N:
            return self.last_payfunc(*process)
        else:
            return (self.p * self.get_step_value(*process, 1) + \
                    self.q * self.get_step_value(*process, 0)) / (1 + self.r)
        
    @property
    def init_value(self):
        return self.get_step_value()
        


def stock_price(s0, u, d, *process):
    """ 记录某个路径下的所有股票价格 
        衍生证券最终支付的辅助函数(如果最终支付与股价有关) """
    s = s0
    yield s
    for step in process:
        s *= pow(u, step) * pow(d, 1 - step)
        yield s
    
# ================= Example 1:   Page 3 例1.1.1看涨期权   =====================
def last_payfunc_1(*process):
    u = 2
    d = 0.5
    s0 = 4
    K = 5
    last_s = list(stock_price(s0, u, d, *process))[-1]
    return max(0, last_s - K)

ed = EuropeanDerivative(2, 0.5, 0.25, 1, last_payfunc_1)
print(ed.init_value)

# ====================== Example 2: Page 12 例1.2.4回望期权  ==================
def last_payfunc_2(*process):
    u = 2
    d = 0.5
    s0 = 4
    s_list = list(stock_price(s0, u, d, *process))
    return max(s_list) - s_list[-1]
    
ed = EuropeanDerivative(2, 0.5, 0.25, 3, last_payfunc_2)
print(ed.init_value)

# ====================== Example 3: Page 13 例1.3.1看跌期权  ==================
def last_payfunc_3(*process):
    u = 2
    d = 0.5
    s0 = 4
    K = 5
    last_s = list(stock_price(s0, u, d, *process))[-1]
    return max(0, K - last_s)
    
ed = EuropeanDerivative(2, 0.5, 0.25, 3, last_payfunc_3)
print(ed.init_value)
