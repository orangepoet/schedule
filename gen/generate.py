# encoding: utf-8
# -*- coding: uft-8 -*-
import sys
from abc import ABCMeta, abstractmethod

from jinja2 import Environment, FileSystemLoader

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
        try:
            template = self.__get_template()
            model = self._get_models()
        except Exception as e:
            raise CodeGenerateException
        else:
            return template.render(model=model)

    def __get_template(self):
        from os.path import join, abspath
        """
        Get template object from package gen, folder templates
        :return: template object
        """
        env = Environment(loader=FileSystemLoader(join(abspath('..'), 'static/templates')))
        return env.get_template(self.template_name)

    @abstractmethod
    def _get_models(self):
        pass


class CodeGenerateException(Exception):
    def __init__(self, *args, **kwargs):
        super(CodeGenerateException, self).__init__(args, kwargs)
