# encoding: utf-8
# -*- coding: uft-8 -*-

from xml.etree import ElementTree as et

from generate import Generator


class ContractGenerator(Generator):
    template_name = 'ctccode.html'

    def __init__(self, dict_contract):
        super(ContractGenerator, self).__init__()
        self.dict_contract = dict_contract

    def _get_models(self):
        ret = []
        ctc = self.dict_contract
        ret.extend(self.__parse_head(ctc["req"]))
        ret.extend(self.__parse_head(ctc["resp"]))
        return ret

    def __parse_head(self, head):
        ret = []
        t = {
            "name": head["name"],
            "prop": self.__get_props(head["items"])
        }
        ret.append(t)
        ret.extend(self.__parse_items(head["items"]))
        return ret

    def __parse_items(self, items):
        ret = []
        if not type(items) is list:
            return ret
        for item in items:
            if not item["children"]:
                continue
            t = {
                "name": item["type"],
                "prop": self.__get_props(item["children"])
            }
            ret.append(t)
            ret.extend(self.__parse_items(item["children"]))
        return ret

    def __get_props(self, items):
        ret = []
        json_desc_format = '[JsonProperty(PropertyName = "{short_name}")]'
        datagram_desc_format = '[DatagramField(Type = FieldType.{field_type}, Require = {require}, Version = {version}, Description = "{desc}"{format})]'
        prop_desc_format = 'public {prop_type} {prop_name} {{ get; set; }}'
        for item in items:
            fmt = ', Format = "{0}"'.format(self.__to_format(item["format"]).replace('\\', '/')) if item[
                "format"] else ''
            cs_type = self.__get_cs_type(item["metadata"], item["type"])

            prop = {
                "json_desc": json_desc_format.format(short_name=item["short_name"]),
                "datagram_desc": datagram_desc_format.format(field_type=item["metadata"],
                                                             require=str.lower(item["require"]),
                                                             version=item["version"],
                                                             desc=self.escape(item["description"]),
                                                             format=fmt),
                "prop_desc": prop_desc_format.format(prop_type=cs_type, prop_name=item['name'])
            }
            ret.append(prop)
        return ret

    @staticmethod
    def escape(attrib_val):
        return str(attrib_val).replace('\\', '/').replace('"', '\\"')

    @staticmethod
    def __to_format(fmt):
        if fmt.find("\\") == -1:
            return fmt
        else:
            return fmt.replace("\\", "/")
        pass

    def __get_cs_type(self, metadata, m_type):
        metadata2 = str.lower(metadata)
        if metadata2 == "dynamic":
            return "string"
        elif metadata2 == "int4" or metadata2 == "int10":
            return "int"
        elif metadata2 == "int20":
            return "long"
        elif metadata2 == "nullableclass" or metadata2 == "class" or metadata2 == "enum":
            return m_type
        elif metadata2 == "list":
            return 'List<{0}>'.format(self.__get_cs_type(m_type, None))
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
        pass


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


def resolve_request(request):
    return {
        "name": request.attrib["name"],
        "type": request.attrib["type"],
        "items": resolve_items(request.findall("item"))
    }


def resolve_response(response):
    return {
        "name": response.attrib["name"],
        "type": response.attrib["type"],
        "items": resolve_items(response.findall("item"))
    }


def resolve(xml_path):
    root = et.parse(xml_path).getroot()
    return {
        "req": resolve_request(root.find("Request")),
        "resp": resolve_response(root.find("Response")),
    }


def main():
    from os.path import exists, join, splitext
    from os import listdir, mkdir
    import time

    dir_root = 'd:/Users/chengz/Desktop/contract'
    dir_xml = join(dir_root, 'xml/dst')
    dir_out = join(dir_root, 'code', time.strftime('%Y%m%dH%H%M'))

    if not exists(dir_xml):
        raise ValueError('dir_xml not exists')

    if not exists(dir_out):
        mkdir(dir_out)
    for file_name in listdir(dir_xml):
        try:
            xml_path = join(dir_xml, file_name)
            dict_contract = resolve(xml_path)
            result = ContractGenerator(dict_contract).generate()
            (file_raw_name, extension) = splitext(file_name)
            file_out = join(dir_out, '{file_name}.txt'.format(file_name=file_raw_name))
            with open(file_out, "w+") as fp:
                fp.write(result)
        except Exception as e:
            print '[error]: generate file {file} failed, message: {message}'.format(file=file_name, message=e.message)
    print 'done'


if __name__ == '__main__':
    main()
