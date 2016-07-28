# encoding: utf-8
# -*- coding: utf-8 -*-
from app import get_config
from gen import render_template, write_file

tpl_name = 'detail_loader.html'
bizname = get_config(__file__, 'bizname')


def main():
    page = render_template(tpl_name=tpl_name, model=bizname)
    if page is not None:
        write_file('{0}CardDetailLoader.cs'.format(bizname), page, 'd:/tmp/out')

    print 'done'


if __name__ == '__main__':
    main()
