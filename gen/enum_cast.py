# encoding: utf-8
# -*- coding: uft-8 -*-

import os

from generate import Generator
from gen import write_out_file, read_in_file_lines


class EnumCodeGenerate(Generator):
    template_name = 'enum_cast.html'

    def __init__(self, model):
        super(EnumCodeGenerate, self).__init__()
        self.__model = model

    def _get_models(self):
        return self.__model


def __get_lines(path):
    with open(path, 'r') as fin:
        return fin.readlines()


def get_enum_name(line):
    fields = line.split()
    if len(fields) == 3:
        return fields[2]
    else:
        index = line.find('enum')
        return line[index + 1].strip()


def x():
    ret = {'name': '', 'enum_items': []}
    lines = read_in_file_lines('enum2.txt')
    ret['name'] = get_enum_name(lines[0])

    for line in lines:
        if '=' in line:
            fields = line.strip().strip(',').split('=')
            if 'unknown' == fields[0].strip().lower():
                continue
            ret['enum_items'].append({
                'name': fields[0],
                'value': fields[1]
            })
    return ret


def main():
    ret = {'name': '', 'enum_items': []}
    lines = read_in_file_lines('enum2.txt')
    ret['name'] = get_enum_name(lines[0])

    for line in lines:
        if '=' in line:
            fields = line.strip().strip(',').split('=')
            if 'unknown' == fields[0].strip().lower():
                continue
            ret['enum_items'].append({
                'name': fields[0],
                'value': fields[1]
            })
    result = EnumCodeGenerate(ret).generate()
    write_out_file('enum_cast.txt', result)

    print 'done'


if __name__ == '__main__':
    main()
