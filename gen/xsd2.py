# encoding: utf-8
# -*- coding: uft-8 -*-

import openpyxl

from gen import write_out_file, CodeGenerateException, render_template

template_name = 'xsd.html'


def get_xsd_type(metadata, ctctype):
    if ctctype is None:
        ret = {
            'dynamic': 'xs:string',
            'int4': 'xs:int',
            'int10': 'xs:int',
            'int20': 'xs:long',
            'boolean': 'xs:boolean',
            'decimal2': 'xs:decimal',
            'decimal6': 'xs:decimal'
        }[str(metadata).lower()]
    else:
        ret = ctctype + 'Type'
    return ret


def get_elements(children):
    ret = []
    for child in children:
        ret.append({
            'name': child.get('short_name'),
            'type': get_xsd_type(child.get('metadata'), child.get('type')),
            'minOccurs': '1' if child.get('required') == 'Y' else '0',
            'maxOccurs': 'unbounded' if 'List' in child.get('metadata') else '1',
            'desc': child.get('remark')
        })
    return ret


def parse_xsd_type(xls_obj):
    ret = []

    children = xls_obj['children']
    if not children:
        return ret

    complex_type = {
        'name': (xls_obj['type'] if xls_obj.has_key('type') else xls_obj['name']) + 'Type',
        'elements': get_elements(children)
    }

    ret.append(complex_type)
    for child in children:
        if child['children']:
            ret.extend(parse_xsd_type(child))
    return ret


def parse_xsd(sheet_data):
    ret = []
    ret.extend(parse_xsd_type(sheet_data['req']))
    ret.extend(parse_xsd_type(sheet_data['resp']))
    return ret


def main():
    import time
    from gen.ctcxml import get_sheet_data

    excel_path = unicode(r'D:\schedule\doc\ctc\6.19\6.19.旅行日程 - 服务接口.xlsx')
    sheet_name = '30302502'

    wb = openpyxl.load_workbook(excel_path)
    sheet = wb.get_sheet_by_name(sheet_name)
    sheet_data = get_sheet_data(sheet)
    xsd_types = parse_xsd(sheet_data)

    try:
        result = render_template(template_name, xsd_types)
    except CodeGenerateException as e:
        print '[CodeGenerateException]: message > {message}'.format(message=e.message)
    except Exception as e:
        print '[Exception]: message > {message}'.format(message=e.message)
    else:
        file_out = 'xsd_{time}.txt'.format(time=time.strftime('%Y%m%dH%H%M'))
    write_out_file(file_out, result)

    print 'done'


if __name__ == '__main__':
    main()
