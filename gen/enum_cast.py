# encoding: utf-8
# -*- coding: uft-8 -*-

from gen import write_out_file, read_as_lines, render_template, CodeGenerateException

template_name = 'enum_cast.html'


def get_enum_name(line):
    fields = line.split()
    if len(fields) == 3:
        return fields[2]
    else:
        index = line.find('enum')
        return line[index + 1].strip()


def main():
    model = {'name': '', 'enum_items': []}
    lines = read_as_lines('enum2.txt')
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
    try:
        result = render_template(template_name, model)
    except CodeGenerateException as e:
        print '[CodeGenerateException]: message > {message}'.format(message=e.message)
    except Exception as e:
        print '[Exception]: message > {message}'.format(message=e.message)
    else:
        write_out_file('enum_cast.txt', result)

    print 'done'


if __name__ == '__main__':
    main()
