# encoding: utf-8
# -*- coding: utf-8 -*-

from gen import render_template, read_as_json, write_file

template_name = 'soaservice.html'


def main():
    model = read_as_json('soaservice.txt')

    result = render_template(template_name, model)
    if result:
        write_file('soaservice.txt', result)


if __name__ == '__main__':
    main()
