# encoding: utf-8
# -*- coding: uft-8 -*-

from app import read_to_lines, write_file, TMP_OUT
from gen import render_template

template_name = 'enumcast.html'


def get_enum_name(line):
    fields = line.split()
    if len(fields) == 3:
        return fields[2]
    else:
        index = line.find('enum')
        return line[index + 1].strip()


def main():
    lines = read_to_lines('enumcast.txt')
    name = get_enum_name(lines[0])
    items = []

    for line in lines:
        if '///' in line and 'summary' not in line:
            desc = line.replace('///', '').strip()
        elif '=' in line:
            fields = line.strip().strip(',').split('=')
            if 'unknown' == fields[0].strip().lower():
                continue
            items.append({
                'name': fields[0].strip(),
                'value': fields[1].strip(),
                'desc': desc
            })
    page = render_template(template_name, name=name, items=items)
    if page is not None:
        write_file('enumcast.txt', page, TMP_OUT)

    print 'done'


if __name__ == '__main__':
    main()
