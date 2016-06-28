# encoding: utf-8
# -*- coding: uft-8 -*-


from json import dumps, loads, load
from os.path import join
from time import strftime

global ROOT
ROOT = 'd:/Users/chengz/Desktop/TestCase/'


def post(server_url, post_url, code, head, body, data_version=5, indented=False, save_result=True):
    from requests import post, codes
    from os.path import join

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
        header = {'Content-Type': 'application/json;charset=UTF-8'}
        resp = post(post_url, json=req, headers=header)
    except Exception as e:
        print '>> ' + e.message
        return None
    else:
        if resp.status_code == codes.ok:
            content = loads(resp.content)
            ret = loads(content['body'])

            root = 'd:/Users/chengz/Desktop/TestCase'
            if save_result:
                json_file = join(root, 'resp',
                                 '{code}({timestamp}).json'.format(code=code, timestamp=strftime('H%H%M%S')))
                with open(json_file, 'w+') as fout:
                    fout.write(dumps(ret))
            return ret
        else:
            print '[error]: status::{status}, message::{message}'.format(status=resp.status_code, message=resp)
            return None


def load_test_case(file_path):
    with open(file_path, 'r') as fp:
        test_case = loads(fp.read())
        return {
            "post_url": test_case['basic']['post_url'],
            "server_url": test_case['basic']['server_url'],
            "service_code": test_case['basic']['service_code'],
            "req_head": test_case['head'],
            "req_body": test_case['body'],
            "expected": test_case['expected']
        }


def do_test_case(test_case, global_config):
    from requests.structures import CaseInsensitiveDict
    resp = post(global_config['server_url'], global_config['post_url'], test_case['service_code'],
                test_case['req_head'], test_case['req_body'])

    resp0 = CaseInsensitiveDict(resp)
    for item in test_case['expected']:
        try:
            # assert resp0
            # assert str(resp0[item]) == str(test_case['expected'][item]), '>> [%s] : expected::%s, actual::%s' % (
            #     item, test_case['expected'][item], resp0[item])
            pass
        except KeyError:
            print '[error] segement::{segement} not found'.format(segement=item)
        except Exception as e:
            print e.message


def get_global_config():
    with open(join(ROOT, 'ini.txt'), 'r') as fp:
        ini = load(fp)
    basic = {
        "server_url": (ini['server_url'][ini['env']]),
        "post_url": ini['post_url']
    }
    return basic


def main():
    from os import walk

    global_config = get_global_config()
    for root, dirs, files in walk(join(ROOT, 'case')):
        for file in files:
            with open(join(root, file), 'r') as fp:
                test_case = load(fp)
                do_test_case(test_case, global_config)


if __name__ == '__main__':
    main()
