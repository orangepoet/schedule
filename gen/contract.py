from xml.etree import ElementTree as et

from gen.generate import Generator


class ContractResolver:
    def __init__(self, xml_file):
        self.xml_path = xml_file

    def resolve(self):
        root = et.parse(self.xml_path).getroot()
        return {
            "req": self.__resolve_request(root.find("Request")),
            "resp": self.__resolve_response(root.find("Response")),
        }

    def __resolve_request(self, request):
        return {
            "name": request.attrib["name"],
            "type": request.attrib["type"],
            "items": self.__resolve_items(request.findall("item"))
        }

    def __resolve_response(self, response):
        return {
            "name": response.attrib["name"],
            "type": response.attrib["type"],
            "items": self.__resolve_items(response.findall("item"))
        }

    def __resolve_items(self, items):
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
                        "children": self.__resolve_items(item.getchildren()) if list else []
                        }
            ret.append(metadata)
        return ret


class ContractGenerator(Generator):
    template_name = 'contract.html'

    def __init__(self, xmlpath):
        """
        :param xmlpath: contract xml path
        """
        super(ContractGenerator, self).__init__()
        self.xml_path = xmlpath

    def _get_models(self):
        resolver = ContractResolver(self.xml_path)
        contract = resolver.resolve()
        return self.__get_model_by_contract(contract)

    def __get_model_by_contract(self, contract):
        ret = []
        ret.extend(self.__parse_head(contract["req"]))
        ret.extend(self.__parse_head(contract["resp"]))
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
        json_desc_format = '[JsonProperty(PropertyName = "%s")]'
        datagram_desc_format = '[DatagramField(Type = FieldType.%s, Require = %s, Version = %s, Description = "%s"%s)]'
        prop_desc_format = 'public %s %s { get; set; }'
        for item in items:
            fmt = ', Format = "{0}"'.format(self.__to_format(item["format"]).replace('\\', '/')) if item[
                "format"] else ''
            cs_type = self.__get_cs_type(item["metadata"], item["type"])

            prop = {
                "json_desc": json_desc_format % (item["short_name"]),
                "datagram_desc": datagram_desc_format % (
                    item["metadata"], str.lower(item["require"]), item["version"],
                    item["description"].replace('\\', '/'), fmt),
                "prop_desc": prop_desc_format % (cs_type, item["name"])
            }
            ret.append(prop)
        return ret

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


def main():
    import os
    import time

    xml_ctc_dir = 'd:/Users/chengz/Desktop/contract'
    in_dir = '%s/%s' % (xml_ctc_dir, 'xml/out/basic')
    out_dir = '%s/%s/%s' % (xml_ctc_dir, 'code', time.strftime('%Y%m%dH%H%M'))

    if not os.path.exists(in_dir):
        raise ValueError('in_dir not found')

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    for file_name in os.listdir(in_dir):
        try:
            xml_path = '%s/%s' % (in_dir, file_name)
            result = ContractGenerator(xml_path).generate()
            (dir_name, file_name) = os.path.split(xml_path)
            (file_raw_name, extension) = os.path.splitext(file_name)
            with open('%s/%s.txt' % (out_dir, file_raw_name), "w+") as fp:
                fp.write(result)
        except Exception as e:
            print('gen file: %s failed, reason: %s' % (file_name, e.message))
    print 'done'


if __name__ == '__main__':
    main()
