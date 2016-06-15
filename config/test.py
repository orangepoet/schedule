# encoding: utf-8
# -*- coding: uft-8 -*-

import os

from requests.structures import CaseInsensitiveDict
from time import strftime
from json import dumps, loads
from requests import post, codes
from xml.etree import ElementTree as et

from utils.files import Files


class ApiTester(object):
    global ROOT
    global HEADER

    ROOT = 'd:/Users/chengz/Desktop/TestCase'
    HEADER = {'Content-Type': 'application/json;charset=UTF-8'}

    def __init__(self, test_file):
        print '>> ' + test_file
        self.file_path = test_file

    def test(self):
        metadata = self.load_metadata()
        resp = ApiTester.post(metadata['server_url'], metadata['post_url'], metadata['service_code'],
                              metadata['req_head'], metadata['req_body'])
        act = CaseInsensitiveDict(resp)
        for item in metadata['expected']:
            try:
                assert str(act[item]) == str(metadata['expected'][item]), '>> [%s] : expected::%s, actual::%s' % (
                    item, metadata['expected'][item], act[item])
            except KeyError:
                print '>> segement:: %s not found' % item
            except Exception as e:
                print e.message

    def load_metadata(self):
        with open(self.file_path, 'r') as fin:
            case_data = loads(fin.read())
            return {
                "post_url": case_data['basic']['post_url'],
                "server_url": case_data['basic']['server_url'],
                "service_code": case_data['basic']['service_code'],
                "req_head": case_data['head'],
                "req_body": case_data['body'],
                "expected": case_data['expected']
            }

    @staticmethod
    def post(server_url, post_url, code, head, body, data_version=5, indented=False, save_result=True):
        head['ServiceCode'] = code
        req = {
            'head': dumps(head),
            'body': dumps(body),
            'code': code,
            'serverUrl': server_url,
            'datagramVersion': data_version,
            'indented': indented
        }
        try:
            resp = post(post_url, json=req, headers=HEADER)
        except Exception as e:
            print '>> ' + e.message
            return None
        else:
            if resp.status_code == codes.ok:
                # print '200 ok'
                content = loads(resp.content)
                ret = loads(content['body'])

                # Save to file
                if save_result:
                    json_file = os.path.join(ROOT, 'resp',
                                             '%s(%s).json' % (code, strftime('H%H%M%S')))
                    with open(json_file, 'w+') as fout:
                        fout.write(dumps(ret))
                return ret
            else:
                print '>> status::%s, message::%s' % (resp.status_code, resp)
                return None


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
