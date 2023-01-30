# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 09:31:37 2022

@author: Angela Lazova
"""

import pandas as pd

my_list = [*range(1,301)]

for num in my_list:
    if len(str(num)) == 1:
        number = '00' + str(num)
    elif len(str(num)) == 2:
        number = '0' + str(num)
    else:
        number = str(num)
        
    data_file = pd.read_csv('csv_spreadsheets/spreadsheet_{}.csv'.format(number))
    data_file.to_excel('xlsx_spreadsheets/spreadsheet_{}.xlsx'.format(number), index=None, header=True)
    