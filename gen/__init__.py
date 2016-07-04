from os.path import join, abspath


def read_in_file_lines(file_name):
    with open(join(abspath('..'), 'static/in', file_name), 'r') as fp:
        return fp.readlines()


def write_out_file(file_name, out):
    with open(join(abspath('..'), 'static/out', file_name), 'w+') as fp:
        fp.write(out)
