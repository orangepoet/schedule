# -*- encoding:utf-8 -*-


class VersionMapEditor(object):
    file_path = 'd:/schedule/src/Schedule.MobileService/SmartTrip/ScheduleApi' \
                '/Server.Web/Config/VersionMapItem/VersionMapItem.smarttrip.xml'
    org_version = 584

    item_format = '  <item systemCode="{}" beginClientVersion="{}" ' \
                  'endClientVersion="9999"  serviceCode="{}" category="1" keyword="{}" value="{}" remark="{}"/>\n'

    def __init__(self):
        self.items = []
        pass

    def append(self, version_item):
        self.items.append(version_item)
        return self

    def save(self):
        for item in self.items:
            lines = []
            code = item.code
            version = item.version
            val = int(item.version) - self.org_version
            keyword = item.keyword
            remark = item.remark

            # append new config
            with open(self.file_path, 'r') as fin:
                for l in fin.readlines():
                    if '<!-- End:   SystemCode=12-->' in l:
                        lines.append(self.item_format.format('12', version, code, keyword, val, remark))
                    elif '<!-- End:   SystemCode=32-->' in l:
                        lines.append(self.item_format.format('32', version, code, keyword, val, remark))
                    elif '<!-- End:   SystemCode=43-->' in l:
                        lines.append(self.item_format.format('43', version, code, keyword, val, remark))
                    lines.append(l)
            # save file
            with open(self.file_path, 'w+') as fout:
                fout.writelines(lines)

    class VersionItem(object):
        code = ''
        version = ''
        keyword = ''
        remark = ''

        def __init__(self, code, version, keyword, remark):
            self.code = code
            self.version = version
            self.keyword = keyword
            self.remark = remark
