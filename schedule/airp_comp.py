# encoding: utf-8
# -*- coding: uft-8 -*-
import re
import sys

from app import get_config

__author__ = 'chengz'

reload(sys)
sys.setdefaultencoding("utf-8")

out_match_file = get_config(__file__, 'out_match_file')
out_unmatched_file = get_config(__file__, 'out_unmatched_file')
in_data_file = get_config(__file__, 'in_data_file')


def is_match(left, right):
    unused = ['楼', '区', '柜台', '岛', '/']
    splicers = [',', '、']

    for word in unused:
        left = left.replace(word, '')
        right = right.replace(word, '')

    if any(x in left for x in splicers):
        for y in re.split('|'.join(splicers), left):
            if is_match(y, right):
                return True
        return False

    if any(x in right for x in splicers):
        for y in re.split('|'.join(splicers), right):
            if is_match(left, y):
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
        else:
            pattern = r'([a-zA-Z]+)([0-9]+)\w*'
            m_left = re.findall(pattern, left)
            m_right = re.findall(pattern, right)
            if len(m_left) > 0 and len(m_left) == len(m_right):
                for p_left, p_right in zip(m_left, m_right):
                    if p_left[0].lstrip('0') != p_right[0].lstrip('0') \
                            or p_left[1].lstrip('0') != p_right[1].lstrip('0'):
                        return False
                return True
            else:
                return False


def main():
    y_set = []
    n_set = []
    with open(in_data_file, 'r') as fp:
        # match_line = [628]
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
    with open(out_match_file, 'w+') as fp:
        fp.writelines(y_set)

    with open(out_unmatched_file, 'w+') as fp:
        fp.writelines(n_set)
    print 'done'


if __name__ == '__main__':
    main()
