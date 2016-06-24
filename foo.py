# encoding: utf-8
# -*- coding: uft-8 -*-
import os
import re
import xlrd

__author__ = 'chengz'

s = 'T101'
left = 'T22'
right = 'T01'


def excel_demo():
    excel_path = os.path.join(os.path.abspath('.'), 'static/input/contract.xlsx')
    excel = xlrd.open_workbook(excel_path)
    # for sheet in excel.sheets():
    #     print sheet
    #     for i in range(sheet.nrows):
    #         print sheet.row_values(i)
    #
    #     break
    sheet = excel.sheet_by_name('30300204')
    if sheet:
        # objs = []
        # obj = set()
        # for i in range(sheet.nrows):
        #     for j in range(sheet.ncols):
        #         cell_value = sheet.cell_value(i, j)
        #         if j == 0 :
        #
        #         if cell_value.strip() == '':
        #             if j == 0 and i > 0:;
        #                 row.append(sheet.cell_value(j, i - 1))
        types = {}
        split_rowno = []
        for i in range(sheet.nrows):
            type_name = sheet.cell_value(i, 0)
            if type_name:
                print type_name, i
                types[type_name] = i

        print types


def string_demo():
    print '212,120'.isalnum()
    print '212,120'.isalpha()
    print '6' in '66b'
    print 'a-b,.\cr'.replace('\-\\\.\,', '')
    print re.split(',|/', 'a,b/c')
    print re.findall(r'([a-zA-Z]+)', 't10b')


def output_enum(biz_type, status_range):
    for status in status_range:
        print 'case {status}:'.format(status=status)
    print '  return BusinessType.{biz_type}'.format(biz_type=biz_type)


def gen_order_status():
    path = 'd:\schedule\src\Schedule.MobileService\SmartTrip\MessagePushJobws\Business\Services\OrderChangeMessagePushService\Models\OrderStatus.cs'
    with open(path, 'r') as fp:
        status_range = []
        for line in fp.readlines():
            if 'enum' in line:
                if status_range:
                    output_enum(biz_type, status_range)
                    del status_range[:]
                biz_type = line[line.index('enum') + 4:].strip()
            elif '=' in line:
                fields = line.rstrip('\n').split('=')
                status_range.append(fields[1].rstrip(','))


if __name__ == '__main__':
    # analyse_order_status()
    # excel_demo()

    arr = [i for i in range(1, 10)]
    print arr[-1]
