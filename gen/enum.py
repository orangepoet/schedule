# encoding: utf-8
# -*- coding: utf-8 -*-

from app import read_to_lines, write_file
from gen import render_template

template_name = 'enum.html'


def main():
    model = []
    for line in read_to_lines('enum.txt'):
        fields = unicode(line).split('=')
        model.append({
            'value': fields[0].strip(' \r\n'),
            'name': fields[1],
            'desc': fields[2].strip(' \r\n')
        })
    page = render_template(template_name, model=model)
    if page:
        write_file('enum.txt', page)

    print 'done'


if __name__ == '__main__':
    main()
