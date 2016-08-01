# encoding: utf-8
# -*- coding: utf-8 -*-

import html

from app import read_to_str, write_file, TMP_OUT, TMP


def main():
    str = read_to_str('soa_req.xml', TMP)
    pattern = '''<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><Request xmlns="http://tempuri.org/"><requestXML>{encode_xml}</requestXML></Request></soap:Body></soap:Envelope>'''
    ret = pattern.format(encode_xml=html.escape(str))
    write_file('soa_req_encode.txt', ret, TMP_OUT)


if __name__ == '__main__':
    main()
