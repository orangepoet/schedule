# encoding: utf-8
# -*- coding: uft-8 -*-

import os

import openpyxl

from generate import Generator


class XsdGenerator(Generator):
    template_name = 'xsd.html'

    def __init__(self, model):
        super(XsdGenerator, self).__init__()
        self.__model = model

    def _get_models(self):
        return self.__model


def get_xsd_type(type):
    if type in ['string', 'int', 'decimal', 'DateTime']:
        return 'xs:' + type
    else:
        return type + 'Type'


def get_elements(children):
    ret = []
    for child in children:
        ret.append({
            'name': child.get('name'),
            'type': get_xsd_type(child.get('type')),
            'minOccurs': '1' if child.get('required') == 'Y' else '0',
            'maxOccurs': 'unbounded' if 'List' in child.get('type') else '1',
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

    excel_path = unicode(r'D:\schedule\doc\ctc\ScheduleExternalApi\ScheduleExternalApi.xlsx')
    sheet_name = 'GetGeofenceRegistrationInfo'

    wb = openpyxl.load_workbook(excel_path)
    sheet = wb.get_sheet_by_name(sheet_name)
    sheet_data = get_sheet_data(sheet)
    xsd_types = parse_xsd(sheet_data)

    result = XsdGenerator(xsd_types).generate()
    output = os.path.join(os.path.abspath('..'), 'static/out',
                          'xsd_{time}.txt'.format(time=time.strftime('%Y%m%dH%H%M')))

    with open(output, "w+") as fp:
        fp.write(result)
    print 'done'


if __name__ == '__main__':
    main()
