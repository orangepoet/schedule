# encoding: utf-8
# -*- coding: uft-8 -*-
import sys

import re

__author__ = 'chengz'

reload(sys)
sys.setdefaultencoding("utf-8")


def is_match(left, right):
    # remove unused chars
    left = left.replace('楼', '').replace('区', '')
    right = right.replace('楼', '').replace('区', '')

    if ',' in left:
        for l in left.split(','):
            if is_match(l, right):
                return True
        return False

    if left == right:
        return True
    # empty string
    elif not left or not right:
        return False
    # both digit
    elif left.isdigit() and right.isdigit():
        return left.lstrip('0') == right.lstrip('0')
    # both alpha
    elif left.isalpha() and right.isalpha():
        return left == right
    # single alpha
    elif left.isalpha() or right.isalpha():
        return left.startswith(right) or right.startswith(left)
    # single digit
    elif left.isdigit() or right.isdigit():
        if left.isdigit():
            m = re.findall(r'\d+', right)
            return m and m[0].lstrip('0') == left
        else:
            m = re.findall(r'\d+', left)
            return m and m[0].lstrip('0') == right
        pass
    # both alphanumeric
    else:
        # a contains b or b contains a, without more digits
        if right in left and left.replace(right, '', 1).isalpha():
            return True
        elif left in right and right.replace(left, '', 1).isalpha():
            return True
        return False


y_set = []
n_set = []
with open('D:/tmp/data(1).txt', 'r') as fp:
    match_line = [717, 2129]
    for index, line in enumerate(fp.readlines()):
        # print line
        line_no = index + 1
        fields = line.split()
        if len(fields) == 4:
            if is_match(fields[2], fields[3]):
                print line_no, 'y: ', fields[2], fields[3]
                y_set.append(line)
            else:
                print line_no, 'n: ', fields[2], fields[3]
                n_set.append(line)
                pass
        else:
            print line_no, 'err: ', line

# save result
with open('d:/tmp/data_y.txt', 'w+') as fp:
    fp.writelines(y_set)

with open('d:/tmp/data_n.txt', 'w+') as fp:
    fp.writelines(n_set)

print 'done'
