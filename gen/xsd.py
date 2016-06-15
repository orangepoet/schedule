from xml.etree import ElementTree as et

import os

from gen.generate import Generator


class XsdGenerator(Generator):
    template_name = 'xsd.html'

    def __init__(self):
        pass

    def _get_models(self):
        root = et.parse(config_file).getroot()
        items = root.findall('item')
        ret = []
        for item in items:
            self.__append_complex_types(item, ret)
        return ret

    def __get_xsd_type(self, metadata, m_type):
        metadata2 = str.lower(metadata)
        if metadata2 == "dynamic":
            return "xs:string"
        elif metadata2 == "int4" or metadata2 == "int10":
            return "xs:int"
        elif metadata2 == "int20":
            return "xs:long"
        elif metadata2 == "nullableclass" or metadata2 == "class" or metadata2 == "enum":
            return m_type
        elif metadata2 == "list":
            return self.__get_xsd_type(m_type, None)
        elif metadata2 == "decimal2" or metadata2 == "decimal6":
            return 'xs:decimal'
        elif metadata2 == "datetime" or metadata2 == "date":
            return 'xs:dateTime'
        elif metadata2 == "boolean":
            return 'xs:boolean'
        elif metadata2 == 'code2':
            return 'xs:string'
        else:
            return metadata
        pass

    def __append_complex_types(self, xnode, ret):
        attrs = xnode.attrib
        cnodes = xnode.findall('item')
        complex_type = {
            'name': attrs['type'] + 'Type',
            'elements': self.__get_elements(cnodes)
        }
        ret.append(complex_type)
        for cnode in cnodes:
            if len(cnode.findall('item')) > 0:
                self.__append_complex_types(cnode, ret)

    def __get_elements(self, xnodes):
        ret = []
        for node in xnodes:
            attrs = node.attrib
            ret.append({
                'name': attrs['shortName'],
                'type': self.__get_xsd_type(attrs['metadata'], attrs['type'] + 'Type'),
                'minOccurs': '0' if attrs['require'] == 'False' else '1',
                'maxOccurs': 'unbounded' if attrs['metadata'] == 'List' else '1',
                'desc': attrs['description']
            })
        return ret

config_file = os.path.join(os.path.abspath('..'), 'gen', 'input', 'xsd_items.xml')


def main():
    import time
    print os.path.abspath('..')

    # result = XsdGenerator().generate()
    # output = os.path.join(os.path.abspath('..'), 'gen', 'output',
    #                       'xsd_{time}.txt'.format(time=time.strftime('%Y%m%dH%H%M')))
    #
    # with open(output, "w+") as fp:
    #     fp.write(result)
    print 'done'


if __name__ == '__main__':
    main()
