# encoding: utf-8
# -*- coding: uft-8 -*-

import os

from generate import Generator


class EnumCodeGenerate(Generator):
    template_name = 'enum_cast.html'

    def __init__(self, enum_file):
        super(EnumCodeGenerate, self).__init__()
        self.__enum_file = enum_file

    def _get_models(self):
        ret = {'name': '', 'enum_items': []}
        lines = self.__get_lines(self.__enum_file)
        ret['name'] = self.__get_enum_name(lines[0])

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

    def __get_lines(self, path):
        with open(path, 'r') as fin:
            return fin.readlines()

    def __get_enum_name(self, line):
        fields = line.split()
        if len(fields) == 3:
            return fields[2]
        else:
            index = line.find('enum')
            return line[index + 1].strip()


def main():
    enum_file = os.path.join(os.path.abspath('..'), 'gen/input/enum.txt')
    result = EnumCodeGenerate(enum_file).generate()
    output = os.path.join(os.path.abspath('.'), 'output', 'enum.txt')
    with open(output, 'w+') as fp:
        fp.write(result)
    print 'done'


if __name__ == '__main__':
    main()
