# encoding: utf-8
# -*- coding: uft-8 -*-

import time
from os import listdir, mkdir
from os.path import exists, join, splitext
from xml.etree import ElementTree as et

from app import get_config, write_file
from gen import render_template

template_name = 'ctccode.html'

DIR_ROOT = get_config(__file__, 'root')


def escape(attrib_val):
    return str(attrib_val).replace('\\', '/').replace('"', '\\"')


def parse_head(head):
    ret = []
    t = {
        "name": head["name"],
        "prop": get_props(head["items"])
    }
    ret.append(t)
    ret.extend(parse_items(head["items"]))
    return ret


def parse_items(items):
    ret = []
    if not type(items) is list:
        return ret
    for item in items:
        if not item["children"]:
            continue
        t = {
            "name": item["type"],
            "prop": get_props(item["children"])
        }
        ret.append(t)
        ret.extend(parse_items(item["children"]))
    return ret


def get_props(items):
    ret = []
    json_desc_format = '[JsonProperty(PropertyName = "{short_name}")]'
    datagram_desc_format = '[DatagramField(Type = FieldType.{field_type}, Require = {require}, Version = {version}, Description = "{desc}"{format})]'
    prop_desc_format = 'public {prop_type} {prop_name} {{ get; set; }}'
    for item in items:
        _format = ', Format = "{format}"'.format(format=escape(item["format"])) if item["format"] else ''
        cs_type = get_cs_type(item["metadata"], item["type"])

        prop = {
            "json_desc": json_desc_format.format(short_name=item["short_name"]),
            "datagram_desc": datagram_desc_format.format(field_type=item["metadata"],
                                                         require=str.lower(item["require"]),
                                                         version=item["version"],
                                                         desc=escape(item["description"]),
                                                         format=_format),
            "prop_desc": prop_desc_format.format(prop_type=cs_type, prop_name=item['name'])
        }
        ret.append(prop)
    return ret


def get_cs_type(metadata, m_type):
    metadata2 = str(metadata).lower()

    if metadata2 == "dynamic":
        return "string"
    elif metadata2 == "int4" or metadata2 == "int10":
        return "int"
    elif metadata2 == "int20":
        return "long"
    elif metadata2 == "nullableclass" or metadata2 == "class" or metadata2 == "enum":
        return m_type
    elif metadata2 == "list":
        return 'List<{0}>'.format(get_cs_type(m_type, None))
    elif metadata2 == "decimal2" or metadata2 == "decimal6":
        return 'decimal'
    elif metadata2 == "dateTime" or metadata2 == "date":
        return 'DateTime'
    elif metadata2 == "boolean":
        return 'bool'
    elif metadata2 == 'code2':
        return 'string'
    else:
        return metadata


def resolve_items(items):
    assert items is not None
    assert type(items) is list

    ret = []
    for item in items:
        attr = item.attrib
        metadata = {"index": attr["index"],
                    "name": attr["name"],
                    "short_name": attr["shortName"],
                    "require": attr["require"],
                    "type": attr["type"],
                    "metadata": attr["metadata"],
                    "description": attr["description"],
                    "version": attr["version"],
                    "format": attr["format"],
                    "children": resolve_items(item.getchildren()) if list else []
                    }
        ret.append(metadata)
    return ret


def resolve_xml_major(xml_major):
    return {
        "name": xml_major.attrib["name"],
        "type": xml_major.attrib["type"],
        "items": resolve_items(xml_major.findall("item"))
    }


def get_ctc_xml_dict(xml_path):
    root = et.parse(xml_path).getroot()

    # req, resp
    return resolve_xml_major(root.find("Request")), resolve_xml_major(root.find("Response"))


def get_ctc_types(xml_path):
    ret = []

    req, resp = get_ctc_xml_dict(xml_path)

    ret.extend(parse_head(req))
    ret.extend(parse_head(resp))
    return ret


def main():
    if not exists(DIR_ROOT):
        mkdir(DIR_ROOT)

    xml_dst_dir = join(DIR_ROOT, 'xml', 'dst')
    if not exists(xml_dst_dir):
        raise ValueError('target xml dir not found: {}'.format(xml_dst_dir))

    code_root_dir = join(DIR_ROOT, 'code')
    if not exists(code_root_dir):
        mkdir(code_root_dir)

    code_out_dir = join(code_root_dir, time.strftime('%Y%m%dH%H%M'))
    if not exists(code_out_dir):
        mkdir(code_out_dir)

    for file_name in listdir(xml_dst_dir):
        model = get_ctc_types(join(xml_dst_dir, file_name))
        page = render_template(template_name, model=model)
        if page:
            (file_raw_name, extension) = splitext(file_name)
            file_name = '{}.txt'.format(file_raw_name)
            write_file(file_name, page, code_out_dir)

    print 'done'


if __name__ == '__main__':
    main()
