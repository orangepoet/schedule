# encoding: utf-8
# -*- coding: utf-8 -*-
import ConfigParser
import os

BARE_DIR = os.path.dirname(__file__)

_configer = ConfigParser.ConfigParser()
_configer.read(os.path.join(BARE_DIR, 'app.ini'))


def get_config(module_file, field):
    (file_raw_name, extension) = os.path.splitext(os.path.basename(module_file))
    section = file_raw_name
    option = field
    return _configer.get(section, option)
