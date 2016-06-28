# encoding: utf-8
# -*- coding: uft-8 -*-
import glob
import os

import shutil
from xml.etree import ElementTree as et


class Files:
    def __init__(self):
        pass

    @staticmethod
    def copy(src_dir, dst_dir, suffix):
        if not os.path.isdir(src_dir):
            raise 'not a directory'

        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)

        for file in glob.iglob(os.path.join(src_dir, suffix)):
            shutil.copy(file, dst_dir)
            print('copy {0} to {1}'.format(file, dst_dir))

    @staticmethod
    def delete(dir, files):
        for f in files:
            os.remove(os.path.join(dir, f))


class SvcDebugger(object):
    m_root = 'd:/schedule/src/Schedule.MobileService/SmartTrip/ScheduleApi/Server.Web/'
    m_config_profile = 'ConfigProfile.xml'
    __global_file = 'Global.asax.cs'

    def __init__(self, env):
        self.__env = env

    def prepare(self):
        self.__config_profile()
        self.__adjust_code()

    def __config_profile(self):
        config_profile = '{}/{}'.format(self.m_root, self.m_config_profile)
        config_tree = et.parse(config_profile)
        root = config_tree.getroot()
        sect_defv = root.find('dev')

        if self.__env == 'fat':
            dst_env = root.find('fat')
        else:
            dst_env = root.find('uat_nt')

        sect_defv.clear()
        for e in dst_env.getchildren():
            sect_defv.append(e)
        config_tree.write(config_profile)

    def __adjust_code(self):
        lines = []
        m_file_path = '%s/%s' % (self.m_root, self.__global_file)
        with open(m_file_path, 'r') as f:
            for index, value in enumerate(f.readlines()):
                if index == 15 or index == 17:  # line number
                    lines.append('//' + value)
                else:
                    lines.append(value)
        with open(m_file_path, 'w+') as f:
            for l in lines:
                f.write(l)
            f.close()


class SvcUpdater(object):
    src_dir = 'd:/schedule/src/Schedule.MobileService/SmartTrip/ScheduleApi'
    dst_dir = 'd:/WebSites/SvcTest'

    def __init__(self):
        pass

    global config

    config = {
        'src': {
            'dir': src_dir,
            'contract_bin': '%s/SmartTrip.DataContract/bin/Release' % src_dir,
            'version_config': '%s/Server.Web/Config/VersionMapItem' % src_dir,
            'service_config': '%s/Server.Web/Config/ServiceItem' % src_dir
        },
        'dst': {
            'dir': dst_dir,
            'bin_dir': '%s/bin' % dst_dir,
            'version_config': '%s/Config/VersionMapItem' % dst_dir,
            'service_config': '%s/Config/ServiceItem' % dst_dir
        }
    }

    def __copy_dll(self):
        try:
            src = config['src']['contract_bin']
            dst = config['dst']['bin_dir']
            Files.copy(src, dst, "*.dll")
            return True
        except:
            print 'copy_dll failed.'
            return False

    def __copy_version_config(self):
        try:
            src = config['src']['version_config']
            dst = config['dst']['version_config']
            Files.copy(src, dst, "*.xml")
            return True
        except:
            print 'copy_version_config failed.'
            return False

    def __copy_service_config(self):
        try:
            src = config['src']['service_config']
            dst = config['dst']['service_config']
            Files.copy(src, dst, "*.xml")
            return True
        except:
            print 'copy_service_config failed.'
            return False

    def upd(self):
        ret = []
        if not self.__copy_dll():
            ret.append('copy all failed')
        if not self.__copy_service_config():
            ret.append('copy service config failed')
        if not self.__copy_version_config():
            ret.append('copy version config failed')
        return ret if len(ret) > 0 else None


def debug():
    print 'env:'
    env = raw_input()
    SvcDebugger(env).prepare()

    print 'done'


def update():
    SvcUpdater().upd()
    print 'done'


def main():
    print 'choose: 1: debug, 2: update'
    case = raw_input()
    if case == '1':
        debug()
    elif case == '2':
        update()
    else:
        print 'invalid'


if __name__ == '__main__':
    main()
