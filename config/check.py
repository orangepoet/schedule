# -*- coding: utf-8 -*-
__author__ = 'chengz'

from os import listdir
from xml.etree import ElementTree as et

current_version = 619
new_contract_dir = r'd:\Users\chengz\Desktop\Contract\xml\dst'


def get_service_config():
    file_path = 'D:\schedule\src\Schedule.MobileService\SmartTrip\ScheduleApi\Server.Web\Config\ServiceItem\ServiceItem.smarttrip.xml'
    root = et.parse(file_path).getroot()
    service_items = root.findall('item')
    return dict(
        [(get_service_short_name(item.attrib['requestClass']), int(item.attrib['serviceName']))
         for item in service_items])


def get_service_short_name(service_class_full_name):
    return service_class_full_name.split(',')[0].split('.')[-1]


def get_service_contract(dir_path, file_name, service_item_config):
    import re
    from os.path import join

    version_set = set()
    file_path = join(dir_path, file_name)
    with open(file_path, 'r') as fp:
        for line in fp.readlines():
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
    if not service_item_config.has_key(req_class_name):
        raise ValueError('request class not config in service_items')

    service_code = service_item_config[req_class_name]
    version_sorted_set = sorted(version_set)
    # print 'check [{file}], code: [{code}], version: {version}'.format(
    #     file=file_name, code=service_code, version=version_sorted_set)
    return (service_code, version_sorted_set)


def check_service_item_map(service_item_map):
    for version, service_lst in service_item_map.iteritems():
        for service, sys_code_lst in service_lst.iteritems():
            if 9 in sys_code_lst:
                continue
            elif 12 not in sys_code_lst:
                print 'warning: ios lose in {service}, version: {version}'.format(service=service, version=version)
            elif 32 not in sys_code_lst:
                print 'warning: android lose in {service}, version: {version}'.format(service=service, version=version)
            elif 43 not in sys_code_lst:
                print 'warning: ipad lose in {service}, version: {version}'.format(service=service, version=version)


def get_version_map_items():
    """Resolve ServiceItem.smarttrip.xml"""

    file_path = 'D:\schedule\src\Schedule.MobileService\SmartTrip\ScheduleApi\Server.Web\Config\VersionMapItem\VersionMapItem.smarttrip.xml'
    root = et.parse(file_path).getroot()
    items = root.findall('item')

    ret = dict()
    for item in items:
        version_val = int(item.attrib['value'])
        service_code = int(item.attrib['serviceCode'])
        sys_code = int(item.attrib['systemCode'])
        begin_version = float(item.attrib['beginClientVersion'])
        end_version = int(item.attrib['endClientVersion'])
        category = int(item.attrib['category'])
        keyword = item.attrib['keyword']
        remark = item.attrib['remark']

        item_string_format = '#item code: {code}, value: {value}, platform: {platform}'.format(code=service_code,
                                                                                               value=version_val,
                                                                                               platform=sys_code)

        # validations
        if sys_code not in [9, 12, 32, 42, 43]:
            raise ValueError('systemCode out of range' + item_string_format)
        if begin_version > 600 and begin_version - 584 != version_val:
            raise ValueError('value not match beginClientVersion' + item_string_format)
        if end_version != 9999:
            raise ValueError('endClientVersion is not 9999' + item_string_format)
        if category != 1:
            raise ValueError('category is not 1' + item_string_format)
        if not keyword:
            raise ValueError('keyword is empty' + item_string_format)
        if not remark:
            raise ValueError('remark is empty' + item_string_format)
        # end validations

        if not ret.has_key(version_val):
            ret[version_val] = dict()
        if not ret[version_val].has_key(service_code):
            ret[version_val][service_code] = []
        ret[version_val][service_code].append(sys_code)

    check_service_item_map(ret)

    return ret


def check_version_map(lst_contract_service_item):
    version_map_items = get_version_map_items()
    for service_tuple in lst_contract_service_item:
        service_code = service_tuple[0]
        versions = service_tuple[1]
        for version in versions:
            if not version_map_items.has_key(version) or not version_map_items[version].has_key(service_code):
                print 'error: ', 'version map lose config, service: {service_code}, version: {version}'.format(
                    service_code=service_code, version=version)

    pass


def get_new_contract_code_list():
    return (current_version, [int(service_code.replace('.xml', '')) for service_code in listdir(new_contract_dir)])


def check_by_contract_code():
    print '--------------------------------------'
    print 'check_by_contract_code'

    service_config = get_service_config()

    contract_dir = 'd:\schedule\src\Schedule.MobileService\SmartTrip\ScheduleApi\SmartTrip.DataContract'
    lst_svc_ver_data = []
    for contract_file in listdir(contract_dir):
        if contract_file.endswith('DataContract.cs') or contract_file.endswith('Contract.cs'):
            try:
                service_contract = get_service_contract(contract_dir, contract_file, service_config)
                lst_svc_ver_data.append(service_contract)
            except Exception as e:
                print 'error: file[{file}] is invalid, msg: {msg}'.format(file=contract_file, msg=e.message)
    if lst_svc_ver_data:
        check_version_map(lst_svc_ver_data)

    print 'check_by_contract_code end'


def get_register_services():
    file_path = 'D:\schedule\src\Schedule.MobileService\SmartTrip\ScheduleApi\Server.Web\Config\ServiceItem\ServiceItem.smarttrip.xml'
    root = et.parse(file_path).getroot()
    service_items = root.findall('item')
    return set(int(item.attrib['serviceName']) for item in service_items)


def check_by_new_contract_xml():
    print '--------------------------------------'
    print 'check_by_new_contract_xml'

    register_services = get_register_services()

    version_map_items = get_version_map_items()
    new_contracts = get_new_contract_code_list()
    version_value = new_contracts[0] - 584
    if not version_map_items.has_key(version_value):
        print 'error: version map lose new service all'
    for service_code in new_contracts[1]:
        if not version_map_items[version_value].has_key(service_code):
            print 'error: version map lose service: {service} in {version}'.format(service=service_code,
                                                                                   version=version_value)
            continue
        platforms = version_map_items[version_value][service_code]
        if platforms is None:
            raise ValueError('platform is empty')
        else:
            for needed in [12, 32, 43]:
                if needed not in platforms:
                    print 'error: verion map lose platform{sys_code}, service: {service}'.format(sys_code=needed,
                                                                                                 service=service_code)
        if service_code not in register_services:
            print 'error: new service not regiter, service code: {svc_code}'.format(svc_code=service_code)

    print 'check_by_new_contract_xml end'


def main():
    check_by_contract_code()
    check_by_new_contract_xml()


if __name__ == '__main__':
    main()
