# encoding: utf-8
# -*- coding: uft-8 -*-
from abc import ABCMeta, abstractmethod

import sys
from jinja2 import Environment, PackageLoader

reload(sys)
sys.setdefaultencoding("utf-8")


class Generator(object):
    __metaclass__ = ABCMeta

    template_name = None

    def __init__(self):
        pass

    def generate(self):
        """
        Generate template file with model
        """
        template = self.__get_template()
        model = self._get_models()
        return template.render(model=model)

    def __get_template(self):
        """
        Get template object from package gen, folder templates
        :return: template object
        """
        env = Environment(loader=PackageLoader('gen', 'templates'))
        return env.get_template(self.template_name)

    @abstractmethod
    def _get_models(self): pass
