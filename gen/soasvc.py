# encoding: utf-8
# -*- coding: utf-8 -*-

from app import read_to_json, write_file
from gen import render_template

template_name = 'soaservice.html'


def main():
    model = read_to_json('soaservice.txt')

    page = render_template(template_name, model=model)
    if page:
        write_file('soaservice.txt', page)


if __name__ == '__main__':
    main()
