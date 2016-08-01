# encoding: utf-8
# -*- coding: utf-8 -*-
from app import get_config, write_file, TMP_OUT
from gen import render_template

tpl_name = 'detail_loader.html'
bizname = get_config(__file__, 'bizname')


def main():
    page = render_template(tpl_name=tpl_name, bizname=bizname)
    if page is not None:
        write_file('{0}CardDetailLoader.cs'.format(bizname), page, TMP_OUT)

    print 'done'


if __name__ == '__main__':
    main()
