# encoding: utf-8
# -*- coding: utf-8 -*-

from gen import render_template, read_as_json, write_out_file, CodeGenerateException

template_name = 'soaservice.html'


def main():
    model = read_as_json('soaservice.txt')

    try:
        result = render_template(template_name, model)
    except CodeGenerateException as e:
        print '[CodeGenerateException]: message > {message}'.format(message=e.message)
    except Exception as e:
        print '[Exception]: message > {message}'.format(message=e.message)
    else:
        if result:
            write_out_file('soaservice.txt', result)


if __name__ == '__main__':
    main()
