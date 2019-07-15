# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:54:48 2017

@author: Christophe
"""

mult3 = filter(lambda x: x % 3 == 0, [1, 2, 3, 4, 5, 6, 7, 8, 9])
sorted([1, 2, 3, 4, 5, 6, 7, 8, 9], key=lambda x: abs(5-x))
f = lambda x: x + 1
f(3)