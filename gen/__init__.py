from os.path import join, abspath

from jinja2 import Environment, FileSystemLoader


class CodeGenerateException(Exception):
    def __init__(self, *args, **kwargs):
        super(CodeGenerateException, self).__init__(args, kwargs)


env = Environment(loader=FileSystemLoader(join(abspath('..'), 'static/templates')))


def read_in_file_lines(file_name):
    with open(join(abspath('..'), 'static/in', file_name), 'r') as fp:
        return fp.readlines()


def write_out_file(file_name, out):
    write_file(join(abspath('..'), 'static/out', file_name), out)


def write_file(file_path, out):
    with open(file_path, 'w+') as fp:
        fp.write(out)


def render_template(tpl_name, model):
    try:
        template = env.get_template(tpl_name)
    except Exception as e:
        raise CodeGenerateException
    else:
        return template.render(model=model)
