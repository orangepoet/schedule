# encoding: utf-8
# -*- coding: uft-8 -*-

from os.path import join
from xml.etree import ElementTree as et

from config import copy

dir_api = 'd:/schedule/src/Schedule.MobileService/SmartTrip/ScheduleApi'
dir_api_web = dir_api + '/Server.Web/'
dir_dst = 'd:/WebSites/SvcTest'
file_config_profile = 'ConfigProfile.xml'
file_global_asax = 'Global.asax.cs'

config = {
    'src': {
        'dir': dir_api,
        'contract_bin': '{dir}/SmartTrip.DataContract/bin/Release'.format(dir=dir_api),
        'version_config': '{dir}/Server.Web/Config/VersionMapItem'.format(dir=dir_api),
        'service_config': '{dir}/Server.Web/Config/ServiceItem'.format(dir=dir_api)
    },
    'dst': {
        'dir': dir_dst,
        'bin_dir': '{dir}/bin'.format(dir=dir_dst),
        'version_config': '{dir}/Config/VersionMapItem'.format(dir=dir_dst),
        'service_config': '{dir}/Config/ServiceItem'.format(dir=dir_dst)
    }
}


class SvcCopyException(Exception):
    def __init__(self, dir):
        super(SvcCopyException, self).__init__()
        self._dir = dir

    @property
    def dir(self):
        return self._dir


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


def copy_dll():
    try:
        src = config['src']['contract_bin']
        dst = config['dst']['bin_dir']
        copy(src, dst, "*.dll")
        return True
    except:
        raise SvcCopyException("dll")


def copy_version_config():
    try:
        src = config['src']['version_config']
        dst = config['dst']['version_config']
        copy(src, dst, "*.xml")
    except:
        raise SvcCopyException('version_map')


def copy_service_config():
    try:
        src = config['src']['service_config']
        dst = config['dst']['service_config']
        copy(src, dst, "*.xml")
    except:
        raise SvcCopyException('service_item')


def debug():
    config_profile()
    adjust_code()


def update():
    try:
        copy_dll()
        copy_service_config()
        copy_version_config()
    except SvcCopyException as e:
        print 'update failed, dir: ' + e.dir


def main():
    print 'choose: 1<debug> 2<update>'
    choice = raw_input()
    if choice == '1':
        debug()
    elif choice == '2':
        update()
    else:
        raise ValueError('invalid choice')

    print 'done'


if __name__ == '__main__':
    main()
