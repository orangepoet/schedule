# encoding: utf-8
# -*- coding: uft-8 -*-

from gen import write_file, read_as_lines, render_template

template_name = 'enumcast.html'


def get_enum_name(line):
    fields = line.split()
    if len(fields) == 3:
        return fields[2]
    else:
        index = line.find('enum')
        return line[index + 1].strip()


def main():
    model = {'name': '', 'enum_items': []}
    lines = read_as_lines('enumcast.txt')
    model['name'] = get_enum_name(lines[0])

    for line in lines:
        if '=' in line:
            fields = line.strip().strip(',').split('=')
            if 'unknown' == fields[0].strip().lower():
                continue
            model['enum_items'].append({
                'name': fields[0].strip(),
                'value': fields[1].strip()
            })
    page = render_template(template_name, model)
    if page is not None:
        write_file('enumcast.txt', page,'d:/tmp/out')

    print 'done'


if __name__ == '__main__':
    main()
