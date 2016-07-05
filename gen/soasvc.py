# encoding: utf-8
# -*- coding: utf-8 -*-

from gen import render_template, read_as_json, write_file

template_name = 'soaservice.html'


def main():
    model = read_as_json('soaservice.txt')

    page = render_template(template_name, model)
    if page:
        write_file('soaservice.txt', page)


if __name__ == '__main__':
    main()
