# encoding: utf-8
# -*- coding: utf-8 -*-

from app import read_to_lines
import re


def main():
    pattern_name_value = 'GetSingleValue(<\w+>)?\("(?P<name>\w+)",\s+"(?P<value>.+)"\)'
    pattern_prop = 'public\s+static\s+\w+\s+(?P<prop>\w+)'
    ret = []

    for line in read_to_lines('config.txt', 'd:/tmp'):
        if '///' in line and 'summary' not in line:
            comment = line.lstrip('///').lstrip().rstrip()
        elif 'public' in line:
            prop_match = re.search(pattern_prop, line)
            prop_name = prop_match.group('prop')
        elif 'BusinessFeatureConfiger' in line:
            name_value_match = re.search(pattern_name_value, line)
            name, value = name_value_match.group('name'), name_value_match.group('value')
            if name <> prop_name:
                raise ValueError('property name not matched with item name')
            ret.append({
                'comment': comment,
                'item_name': name,
                'item_value': name_value_match.group('value')
            })

    str_format = '''
if exists (select count(1) from BusinessFeatureItem where ItemName='{name}')
  update BusinessFeatureItem set ItemValue='{value}', Remark='{comment}' where ItemName='{name}'
else
  insert into BusinessFeatureItem (ItemName,ItemValue,Remark) values('{name}','{value}','{comment}')
'''
    print 'go'
    print 'use SCHSmartTripDB'
    for item in ret:
        print str_format.format(name=item['item_name'], value=item['item_value'], comment=item['comment'])

    print 'go'


if __name__ == '__main__':
    main()
