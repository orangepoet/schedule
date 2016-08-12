# encoding: utf-8
# -*- coding: uft-8 -*-
from os import listdir, walk
from os.path import join

from gen.ctccode import get_ctc_xml_dict

xml_dir = r'D:\tmp\ctc\xml\20160810H1514'


def append2dict(items):
    ret = dict()
    for item in items:
        if item['type'] and item['children']:
            ret[item['type']] = item
    return ret


def append2dict2(items):
    ret = dict()
    for item in items:
        if item['type'] and not item['children']:
            ret[item['type']] = item
    return ret


def main():
    # take missing type from ref files
    # (condition) if miss type not contained in new xml contract
    # then fetch from old xml contract file and insert into new
    # save
    item_types = dict()
    xml_dir_ref = join(xml_dir, 'ref')
    for file in listdir(xml_dir_ref):
        xml_path = join(xml_dir_ref, file)
        req, resp = get_ctc_xml_dict(xml_path)
        item_types.update(append2dict(req['items']))
        item_types.update(append2dict(resp['items']))

    missing_types = dict()
    for file in listdir(xml_dir):
        if file.endswith('.xml'):
            xml_path = join(xml_dir, file)
            req, resp = get_ctc_xml_dict(xml_path)
            missing_types.update(append2dict2(req['items']))
            missing_types.update(append2dict2(resp['items']))

    for k, v in missing_types.iteritems():
        if not item_types.has_key(k):
            print 'miss2', k
        else:
            print 'amend', k


if __name__ == '__main__':
    main()
