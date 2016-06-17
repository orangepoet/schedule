# -*- coding: utf-8 -*-
__author__ = 'chengz'

import xlrd

table = xlrd.open_workbook('d:/tmp/Analyse/datafix-6.14&6.15_chengz.xlsx')
sheet = table.sheet_by_index(0)
nrows = sheet.nrows
print nrows