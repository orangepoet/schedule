# encoding: utf-8
# -*- coding: utf-8 -*-
from gen import read_as_lines, write_out_file, render_template, CodeGenerateException

template_name = 'enum.html'


def main():
    ret = []
    for line in read_as_lines('enum.txt'):
        fields = unicode(line).split('=')
        ret.append({
            'value': fields[0].strip(' \r\n'),
            'name': fields[1],
            'desc': fields[2].strip(' \r\n')
        })
    try:
        outs = render_template(template_name, ret)
    except CodeGenerateException as e:
        print '[CodeGenerateException]: message > {message}'.format(message=e.message)
    except Exception as e:
        print '[Exception]: message > {message}'.format(message=e.message)
    else:
        write_out_file('enum.txt', outs)

    print 'done'


if __name__ == '__main__':
    main()
