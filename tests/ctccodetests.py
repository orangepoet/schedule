# encoding: utf-8
# -*- coding: utf-8 -*-

import unittest

from mock import MagicMock

import gen.ctccode as client
import foo as client2


class CTCCodeTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_cs_type(self):
        cs_type = client.get_cs_type(metadata='Dynamic', m_type=None)
        self.assertEquals(cs_type, 'string')

        cs_type = client.get_cs_type(metadata='Int4', m_type=None)
        self.assertEquals(cs_type, 'int')

        cs_type = client.get_cs_type(metadata='Int10', m_type=None)
        self.assertEquals(cs_type, 'int')

        cs_type = client.get_cs_type(metadata='Decimal6', m_type=None)
        self.assertEquals(cs_type, 'decimal')

        cs_type = client.get_cs_type(metadata='NullableClass', m_type='WayInformation')
        self.assertEquals(cs_type, 'WayInformation')

        cs_type = client.get_cs_type(metadata='List', m_type='MapCarRecommendInformation')
        self.assertEquals(cs_type, 'List<MapCarRecommendInformation>')

        cs_type = client.get_cs_type(metadata='Int20', m_type=None)
        self.assertEquals(cs_type, 'long')

    def test_get_ctc_types(self):
        mock_xml_dict = {
            'req': {
                'name': 'MyRequest',
                'items': []
            },
            'resp': {
                'name': 'MyResponse',
                'items': []
            }
        }
        client.get_ctc_xml_dict = MagicMock(return_value=mock_xml_dict)
        models = client.get_ctc_types('some path')
        self.assertIsNotNone(models)

    def test_foo(self):
        client2.method1 = MagicMock(return_value=10)
        ret = client2.method2(1)
        self.assertEquals(ret, 20)


if __name__ == '__main__':
    unittest.main()
