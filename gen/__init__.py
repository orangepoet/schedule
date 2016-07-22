# encoding: utf-8
# -*- coding: uft-8 -*-

import sys
from json import load
from os.path import join, exists

from jinja2 import Environment, FileSystemLoader

from app import BARE_DIR

reload(sys)
sys.setdefaultencoding("utf-8")

env = Environment(loader=FileSystemLoader(join(BARE_DIR, 'static/templates')))


def read_as_lines(file_name, dir_path='in'):
    if dir_path == 'in':
        file_path = join(BARE_DIR, 'static/in', file_name)
    else:
        if not exists(dir_path):
            raise ValueError('dir path not exists')
        file_path = join(dir_path, file_name)
    with open(file_path, 'r') as fp:
        return fp.readlines()


def read_as_json(file_name, dir_path='in'):
    if dir_path == 'in':
        file_path = join(BARE_DIR, 'static/in', file_name)
    else:
        if not exists(dir_path):
            raise ValueError('dir path not exists')
        file_path = join(dir_path, file_name)
    with open(file_path, 'r') as fp:
        return load(fp)


def write_file(file_name, out, dir_path='out'):
    if dir_path == 'out':
        file_path = join(BARE_DIR, 'static/out', file_name)
    else:
        if not exists(dir_path):
            raise ValueError('dir path not exists')
        file_path = join(dir_path, file_name)
    with open(file_path, 'w+') as fp:
        fp.write(out)


def render_template(tpl_name, model):
    """
    Jinja2 render method wrapper, template + model => page, no throwable
    :param tpl_name: template name
    :param model: model data
    :return: string representation of generated page
    """
    try:
        template = env.get_template(tpl_name)
        return template.render(model=model)
    except Exception as e:
        print '[error], method: [render_template], message: [{message}]'.format(message=e.message)
    return None
