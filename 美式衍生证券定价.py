# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:17:09 2019

@author: Administrator
"""
from functools import partial


class AmericanDerivative:
    """ 求解美式 路径依赖 衍生证券的期初价值 """
    
    def __init__(self, up, down, free_risk, steps, pay_funcs):
        """ 股票二叉树框架 : 0 < d < 1 + r < u 
        pay_funcs是每期立即行权的支付  列表
        """
        assert 0 < down < 1 + free_risk < up
        self.u = up
        self.d = down
        self.r = free_risk
        self.N = steps
        self.pay_funcs = pay_funcs
        self.p = (1 + free_risk - down) / (up - down)
        self.q = (up - 1 - free_risk) / (up - down)
    
    def get_step_value(self, *process):
        """ 各路径下的衍生品价值
        比如 get_step_value(0,1,1) 表示已知股票下跌上涨上涨时衍生品价值 
        见 Page10 V的递推公式 """
        if len(process) == self.N:
            return max(0, self.pay_funcs[-1](*process))
        else:
            return max(self.pay_funcs[len(process)](*process),
                    (self.p * self.get_step_value(*process, 1) + \
                    self.q * self.get_step_value(*process, 0)) / (1 + self.r))
        
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
    
# ================= Example : Page 103 习题4.3   =====================
u = 2
d = 0.5
r = 0.25
s0 = 4
K = 4
steps = 3
def pay_func_helper(i, *process):
    stock_list = list(stock_price(s0, u, d, *process))
    return K - sum(stock_list) / (1 + i)

pay_funcs = [partial(pay_func_helper, i) for i in range(1 + steps)]

ad = AmericanDerivative(u, d, r, steps, pay_funcs)
print(ad.init_value)
