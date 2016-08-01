# encoding: utf-8
# -*- coding: uft-8 -*-

import openpyxl

from app import get_config, write_file, TMP_OUT
from gen import render_template
from gen.ctcxml import get_sheet_data

template_name = 'xsd.html'
excel_path = unicode(get_config(__file__, 'excel_path'))
sheet_name = get_config(__file__, 'sheet_name')


def get_xsd_type(metadata, ctc_type):
    if ctc_type is None:
        ret = {
            'string': 'xs:string',
            'int': 'xs:int',
            'bool': 'xs:boolean',
            'datetime': 'xs:dateTime',
            'long': 'xs:long',
            'decimal': 'xs:decimal',
            'decimal6': 'xs:decimal'
        }[str(metadata).lower()]
    else:
        ret = ctc_type + 'Type'
    return ret


def get_elements(children):
    ret = []
    for child in children:
        ret.append({
            'name': child.get('name'),
            'type': get_xsd_type(child.get('metadata'), child.get('type')),
            'minOccurs': '1' if child.get('required') == 'Y' else '0',
            'maxOccurs': 'unbounded' if is_unbound(child.get('metadata')) else '1',
            'desc': child.get('remark')
        })
    return ret


def is_unbound(metadata):
    if not isinstance(metadata, basestring):
        return False
    return metadata.lower() in ('list', 'array')


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


def append_request_head(request):
    request['elements'].insert(0, {
        'name': 'head',
        'type': 'mobileCommon:MobileRequestHead',
        'minOccurs': '1',
        'maxOccurs': '1',
        'desc': unicode('请求头部')
    })


def append_response_status(response):
    response['elements'].insert(0, {
        'name': 'ResponseStatus',
        'type': 'common:ResponseStatusType',
        'minOccurs': '1',
        'maxOccurs': '1',
        'desc': unicode('服务响应状态')
    })


def post_execute(complex_types):
    for ct in complex_types:
        if ct['name'].endswith('RequestType'):
            append_request_head(ct)
        elif ct['name'].endswith('ResponseType'):
            append_response_status(ct)
    pass


def get_xsd_types(req, resp):
    xsd_types = []
    xsd_types.append(req)
    xsd_types.append(resp)
    post_execute(xsd_types)
    return xsd_types


def main():
    """
    针对H5Api.xlsx 生成XSD代码
    """
    wb = openpyxl.load_workbook(excel_path)
    sheet = wb.get_sheet_by_name(sheet_name)
    req, resp = get_sheet_data(sheet)

    xsd_types = get_xsd_types(req, resp)
    page = render_template(template_name, model=xsd_types)
    if page is not None:
        write_file('xsd_{0}.txt'.format(sheet_name), page, TMP_OUT)

    print 'done'


if __name__ == '__main__':
    main()
