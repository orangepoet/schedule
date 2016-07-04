# encoding: utf-8
# -*- coding: utf-8 -*-
from generate import Generator


class SoaServiceGenerator(Generator):
    template_name = 'soaservice.html'

    def __init__(self, model):
        super(SoaServiceGenerator, self).__init__()
        self.__model = model

    def _get_models(self):
        return self.__model


def main():
    from os.path import join, abspath
    from json import load

    in_path = join(abspath('..'), 'static/in/soaservice.txt')
    with open(in_path, 'r') as fp:
        model = load(fp)

    result = SoaServiceGenerator(model).generate()
    out_path = join(abspath('..'), 'static/out/soaservice.txt')
    with open(out_path, 'w+') as fp:
        fp.write(result)


if __name__ == '__main__':
    main()
