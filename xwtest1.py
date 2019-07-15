# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 11:28:20 2016

@author: Christophe
"""

import xlwings as xw
import pandas as pd
df =pd.DataFrame([[1,2], [3,4]], columns=['a', 'b'])
xw.Workbook('Classeur1')
xw.Range('A1').value = df
xw.range('A1').options(pd.DataFrame, expand='table').value