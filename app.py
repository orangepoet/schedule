# encoding: utf-8
# -*- coding: utf-8 -*-
import ConfigParser
import os
from genericpath import exists
from json import load
from os.path import join

BARE_DIR = os.path.dirname(__file__)

_configer = ConfigParser.ConfigParser()
_configer.read(os.path.join(BARE_DIR, 'app.ini'))


def get_config(module_file, field):
    (file_raw_name, extension) = os.path.splitext(os.path.basename(module_file))
    section = file_raw_name
    option = field
    return _configer.get(section, option)


TMP = get_config(__file__, 'tmp')
TMP_OUT = get_config(__file__, 'tmp_out')


def read_to_json(file_name, dir_path='in'):
    if dir_path == 'in':
        file_path = join(BARE_DIR, 'static/in', file_name)
    else:
        if not exists(dir_path):
            raise ValueError('dir path not exists')
        file_path = join(dir_path, file_name)
    with open(file_path, 'r') as fp:
        return load(fp)


def read_to_lines(file_name, dir_path='in'):
    if dir_path == 'in':
        file_path = join(BARE_DIR, 'static/in', file_name)
    else:
        if not exists(dir_path):
            raise ValueError('dir path not exists')
        file_path = join(dir_path, file_name)
    with open(file_path, 'r') as fp:
        return fp.readlines()


def read_to_str(file_name, dir_path='in'):
    if dir_path == 'in':
        file_path = join(BARE_DIR, 'static/in', file_name)
    else:
        if not exists(dir_path):
            raise ValueError('dir path not exists')
        file_path = join(dir_path, file_name)
    with open(file_path, 'r') as fp:
        return fp.read()


def write_file(file_name, buffer, dir_path='out'):
    if dir_path == 'out':
        file_path = join(BARE_DIR, 'static/out', file_name)
    else:
        if not exists(dir_path):
            raise ValueError('dir path not exists')
        file_path = join(dir_path, file_name)
    with open(file_path, 'w+') as fp:
        fp.write(buffer)
