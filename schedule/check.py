# encoding: utf-8
# -*- coding: utf-8 -*-

import re
from os import listdir
from xml.etree import ElementTree as et

from app import get_config, read_to_lines

current_version = int(get_config(__file__, 'version'))
dir_contract_xml = get_config(__file__, 'dir_contract_xml')
dir_contract = get_config(__file__, 'dir_contract')
path_service_items = get_config(__file__, 'path_service_items')
path_version_map = get_config(__file__, 'path_version_map')


def get_version_value(version):
    version_min_value = 584
    return int(version) - version_min_value


def read_contract_file(dir, filename, request_service_map):
    '''读取契约文件'''

    version_set = set()
    for line in read_to_lines(filename, dir):
        if 'DatagramField' in line:
            match = re.search('\s*\[DatagramField.*Version\s=\s(?P<ver>\d+).*\]\s*', line)
            if match:
                version = int(match.group('ver'))
                if version > 0:
                    version_set.add(version)
        elif 'class' in line and 'Request' in line:
            match = re.search('\s*public[\s+\w+]*class\s+(?P<req_name>\w+)\s*', line)
            req_class_name = match.group('req_name')
    if not req_class_name:
        raise ValueError('request class not found')
    if not request_service_map.has_key(req_class_name):
        raise ValueError('request class not config in service_items')

    return request_service_map[req_class_name], sorted(version_set)


def read_version_map_items():
    '''读取version_map配置文件'''

    root = et.parse(path_version_map).getroot()
    items = root.findall('item')

    ret = dict()
    for item in items:
        version_value, service_code, sys_code, begin_version, end_version, category, keyword, remark = \
            int(item.attrib['value']), \
            int(item.attrib['serviceCode']), \
            int(item.attrib['systemCode']), \
            float(item.attrib['beginClientVersion']), \
            int(item.attrib['endClientVersion']), \
            int(item.attrib['category']), \
            item.attrib['keyword'], \
            item.attrib['remark']

        validate_version_map_item(begin_version, category, end_version, keyword, remark, service_code, sys_code,
                                  version_value)

        if not ret.has_key(version_value):
            ret[version_value] = dict()
        if not ret[version_value].has_key(service_code):
            ret[version_value][service_code] = []
        ret[version_value][service_code].append(sys_code)

    validate_version_map(ret)
    return ret


def read_contract_dir(dir):
    '''读取契约code文件夹'''

    request_service_map = dict([(request_class_name(item.attrib['requestClass']), int(item.attrib['serviceName']))
                                for item in read_service_items()])

    ret = []
    for file in listdir(dir):
        if file.endswith('Contract.cs'):
            try:
                service_versions = read_contract_file(dir, file, request_service_map)
                ret.append(service_versions)
            except Exception as e:
                print 'error: file[{file}] is invalid, msg: {msg}'.format(file=file, msg=e.message)
    return ret


def read_service_items():
    '''读取ServiceItem配置文件'''

    root = et.parse(path_service_items).getroot()
    return root.findall('item')


def validate_version_map_item(begin_version, category, end_version, keyword, remark, service_code, sys_code,
                              version_value):
    item_string_format = '#item code: {code}, value: {value}, platform: {platform}' \
        .format(code=service_code, value=version_value, platform=sys_code)
    if sys_code not in [9, 12, 32, 42, 43]:
        raise ValueError('systemCode out of range' + item_string_format)
    if begin_version > 600 and get_version_value(begin_version) != version_value:
        raise ValueError('value not match beginClientVersion' + item_string_format)
    if end_version != 9999:
        raise ValueError('endClientVersion is not 9999' + item_string_format)
    if category != 1:
        raise ValueError('category is not 1' + item_string_format)
    if not keyword:
        raise ValueError('keyword is empty' + item_string_format)
    if not remark:
        raise ValueError('remark is empty' + item_string_format)


def validate_version_map(service_item_map):
    for version, svc_codes in service_item_map.iteritems():
        for service, sys_code_lst in svc_codes.iteritems():
            if 9 in sys_code_lst:
                # continue
                pass
            elif 12 not in sys_code_lst:
                print 'warning: ios lose in {service}, version: {version}'.format(service=service, version=version)
            elif 32 not in sys_code_lst:
                print 'warning: android lose in {service}, version: {version}'.format(service=service, version=version)
            elif 43 not in sys_code_lst:
                print 'warning: ipad lose in {service}, version: {version}'.format(service=service, version=version)


def request_class_name(class_full_name):
    '''解析ServiceItem.xml中的类全名'''

    pattern = 'Ctrip\.Mobile\.Server\.SmartTrip\.DataContract\.(?P<req_class_name>\w+), Ctrip.Mobile.Server.SmartTrip.DataContract'
    match = re.search(pattern, class_full_name)
    if match is None:
        raise ValueError('error: request class full name not correct')
    return match.group('req_class_name')


def comp_with_contract_code():
    '''将契约生成代码和version_map做对比'''

    print 'check_by_contract_code'
    print '--------------------------------------'

    ctc_service_versions = read_contract_dir(dir_contract)
    version_map_items = read_version_map_items()

    if ctc_service_versions and version_map_items:
        for service_versions in ctc_service_versions:
            service_code, versions = service_versions[0], service_versions[1]
            for version in versions:
                if not version_map_items.has_key(version) or not version_map_items[version].has_key(service_code):
                    print 'error: ', 'version map lose config, service: {service_code}, version: {version}'.format(
                        service_code=service_code, version=version)

    print '--- end ---\n'


def comp_with_ctcxml_dst():
    '''将ctcxml/dst文件夹和version_map做对比'''

    print 'check_by_new_contract_xml'
    print '--------------------------------------'

    register_services = set(int(item.attrib['serviceName']) for item in read_service_items())

    version_map_items = read_version_map_items()
    new_service_codes = [int(service_code.rstrip('.xml')) for service_code in listdir(dir_contract_xml)]
    current_version_value = get_version_value(current_version)

    if not version_map_items.has_key(current_version_value):
        print 'error: version map lose new service all'
    for service_code in new_service_codes:
        if not version_map_items[current_version_value].has_key(service_code):
            print 'error: version map lose service: {service} in {version}'.format(service=service_code,
                                                                                   version=current_version_value)
            continue
        platforms = version_map_items[current_version_value][service_code]
        if platforms is None:
            raise ValueError('platform is empty')
        else:
            for sys_code in [12, 32, 43]:
                if sys_code not in platforms:
                    print 'error: verion map lose platform{sys_code}, service: {service}'.format(sys_code=sys_code,
                                                                                                 service=service_code)
        if service_code not in register_services:
            print 'error: new service not regiter, service code: {svc_code}'.format(svc_code=service_code)

    print '--- end ---\n'


def main():
    print 'current version: ', get_version_value(current_version), '\n'

    comp_with_contract_code()
    comp_with_ctcxml_dst()


if __name__ == '__main__':
    main()
