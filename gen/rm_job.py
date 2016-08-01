# encoding: utf-8
# -*- coding: utf-8 -*-

from app import get_config, write_file, TMP_OUT
from gen import render_template

TABLE_NAME = get_config(__file__, 'table_name')


def render_job(table_name):
    template_name = 'rm_job.html'
    page = render_template(template_name, table_name)
    if page is None:
        print 'error: render_job comes across problem'
    write_file('{0}DeleteJob.cs'.format(table_name), page, TMP_OUT)


def render_service(table_name):
    template_name = 'rm_service.html'
    page = render_template(template_name, table_name)
    if page is None:
        print 'error: render_service comes across problem'
    write_file('{0}DeleteService.cs'.format(table_name), page, TMP_OUT)


def render_logger(table_name):
    template_name = 'remove_logger.html'
    page = render_template(template_name, table_name)
    if page is None:
        print 'error: render_logger comes across problem'
    write_file('{0}RemoveLogger.cs'.format(table_name), page, TMP_OUT)


def render_handler(table_name):
    template_name = 'remove_handler.html'
    page = render_template(template_name, table_name)
    if page is None:
        print 'error: render_handler comes across problem'
    write_file('{0}RemoveHandler.cs'.format(table_name), page, TMP_OUT)


def render_repo():
    import repo
    repo.render_repo()


def main():
    render_job(TABLE_NAME)
    render_service(TABLE_NAME)
    render_logger(TABLE_NAME)
    render_handler(TABLE_NAME)
    render_repo()

    print 'done'


if __name__ == '__main__':
    main()
