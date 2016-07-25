# encoding: utf-8
# -*- coding: utf-8 -*-
import ConfigParser
import os

BARE_DIR = os.path.dirname(__file__)

_configer = ConfigParser.ConfigParser()
_configer.read(os.path.join(BARE_DIR, 'app.ini'))


def get_config(module_file, field):
    section = os.path.basename(module_file).rstrip('.py')
    option = field
    return _configer.get(section, option)
