# encoding: utf-8
# -*- coding: utf-8 -*-
from gen import read_in_file_lines, write_out_file
from generate import Generator


class EnumGenerator(Generator):
    template_name = 'enum.html'

    def __init__(self, model):
        super(EnumGenerator, self).__init__()
        self.__model = model

    def _get_models(self):
        return self.__model


def main():
    ret = []
    for line in read_in_file_lines('enum.txt'):
        fields = unicode(line).split('=')
        ret.append({'value': fields[0].strip(' \r\n'), 'name': fields[1], 'desc': fields[2].strip(' \r\n')})
    outs = EnumGenerator(ret).generate()
    write_out_file('enum.txt', outs)


if __name__ == '__main__':
    main()
