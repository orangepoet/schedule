# encoding: utf-8
# -*- coding: uft-8 -*-

import sys
from os.path import join

from jinja2 import Environment, FileSystemLoader

from app import BARE_DIR

reload(sys)
sys.setdefaultencoding("utf-8")

env = Environment(loader=FileSystemLoader(join(BARE_DIR, 'static/templates')))


def render_template(tpl_name, **context):
    """
    Jinja2 render method wrapper, template + model => page, no throwable
    :param tpl_name: template name
    :return: string representation of generated page
    """
    try:
        template = env.get_template(tpl_name)
        return template.render(context)
    except Exception as e:
        print '[error], method: [render_template], message: [{message}]'.format(message=e.message)
    return None
