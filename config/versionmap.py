# -*- encoding:utf-8 -*-
# -*- coding: uft-8 -*-


file_path = 'd:/schedule/src/Schedule.MobileService/SmartTrip/ScheduleApi' \
            '/Server.Web/Config/VersionMapItem/VersionMapItem.smarttrip.xml'
item_format = unicode('  <item systemCode="{item[system_code]}" beginClientVersion="{item[version]}" ' \
                      'endClientVersion="9999"  serviceCode="{item[service_code]}" category="1" keyword="{item[keyword]}" value="{item[value]}" remark="{item[remark]}"/>\n')


def to_items(items, sys_code):
    ret = []
    for item in items:
        item['system_code'] = sys_code
        item_str = item_format.format(item=item)
        ret.append(item_str.encode('utf-8'))
    return ret


def new_items():
    from json import load
    from os.path import join, abspath

    version_min = 584

    version_map_path = join(abspath('..'), 'static/in/version_map.txt')
    with open(version_map_path, 'r') as fp:
        ret = load(fp)
        if ret:
            for item in ret:
                item['value'] = item['version'] - version_min
    return ret


def main():
    lines = []
    items = new_items()

    with open(file_path, 'r') as fp:
        for line in fp.readlines():
            if '<!-- End:   SystemCode=12-->' in line:
                lines.extend(to_items(items, 12))
            elif '<!-- End:   SystemCode=32-->' in line:
                lines.extend(to_items(items, 32))
            elif '<!-- End:   SystemCode=43-->' in line:
                lines.extend(to_items(items, 43))
            lines.append(line)

    with open(file_path, 'w+') as fp:
        fp.writelines(lines)


if __name__ == '__main__':
    main()