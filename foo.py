# -*- coding: utf-8 -*-
import re

__author__ = 'chengz'

# with open('D:\Users\chengz\Desktop\chengz.csv', 'r') as fp:
#     for line in fp.readlines():
#         fields = line.split(',')
#         if len(fields) == 4:
#             if fields[2] == fields[3]:
#                 print line
#         else:
#             print line
index = 'orangepoet'.find('xx')
# print index
#
# print '008'.isdigit()
# print '008'.lstrip('0')
# print ''.isalpha()
# print 'T1'.replace('0', '#')

s = 'T101'
left = 'T22'
right = 'T01'
# print re.findall(r'([a-zA-Z]*)(0*[1-9]{1,})([a-zA-Z]*)', left)
# print re.findall(r'([a-zA-Z]*)(0*[1-9]{1,})([a-zA-Z]*)', right)

print '212,120'.isalnum()
print '212,120'.isalpha()
print '6' in '66b'
print 'a-b,.\cr'.replace('\-\\\.\,','')

print re.findall(r'([a-zA-Z]+)','t10b')