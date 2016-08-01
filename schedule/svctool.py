# encoding: utf-8
# -*- coding: uft-8 -*-

from os.path import join
from xml.etree import ElementTree as et

from schedule import copy

dir_api = 'd:/schedule/src/Schedule.MobileService/SmartTrip/ScheduleApi'
dir_api_web = dir_api + '/Server.Web/'
dir_dst = 'd:/WebSites/SvcTest'
file_config_profile = 'ConfigProfile.xml'
file_global_asax = 'Global.asax.cs'

config = {
    'src': {
        'dir': dir_api,
        'bin': join(dir_api, 'SmartTrip.DataContract/bin/Release'),
        'version_map': join(dir_api, 'Server.Web/Config/VersionMapItem'),
        'service_item': join(dir_api, 'Server.Web/Config/ServiceItem')
    },
    'dst': {
        'dir': dir_dst,
        'bin': join(dir_dst, 'bin'),
        'version_map': join(dir_dst, 'Config/VersionMapItem'),
        'service_item': join(dir_dst, 'Config/ServiceItem')
    }
}


def config_profile(env):
    file_path = join(dir_api_web, file_config_profile)
    config_tree = et.parse(file_path)
    root = config_tree.getroot()
    sect_defv = root.find('dev')

    if env == 'fat':
        dst_env = root.find('fat')
    elif env == 'uat':
        dst_env = root.find('uat_nt')
    else:
        raise ValueError('env is invalid')

    sect_defv.clear()
    for e in dst_env.getchildren():
        sect_defv.append(e)
    config_tree.write(file_path)


def adjust_code():
    lines = []

    m_file_path = join(dir_api_web, file_global_asax)
    with open(m_file_path, 'r') as fp:
        for line in fp.readlines():
            if 'ThreadPool.SetMaxThreads' in line and not '//' in line:
                lines.append('//' + line)
            elif 'PreparedCacheManager' in line and not '//' in line:
                lines.append('//' + line)
            else:
                lines.append(line)
    with open(m_file_path, 'w+') as fp:
        for l in lines:
            fp.write(l)


def update():
    for src, dst in zip(config['src'].iteritems(), config['dst'].iteritems()):
        if src[0] == 'bin':
            copy(src[1], dst[1], '*.dll')
        elif src[0] == 'version_map' or src[0] == 'service_item':
            copy(src[1], dst[1], '*.xml')


def debug():
    print 'env> 1: fat, 2:uat'
    input = raw_input()
    if input == '1':
        env = 'fat'
    elif input == '2':
        env = 'uat'
    else:
        raise ValueError('invalid env')
    config_profile(env)
    adjust_code()


def main():
    print 'command> 1: debug, 2:update'
    command = int(raw_input())
    if command == 1:
        debug()
    elif command == 2:
        update()
    else:
        print 'command not found'

    print 'done'


if __name__ == '__main__':
    main()
