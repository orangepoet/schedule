import re


class Mapper(object):
    left_path = 'd:/tmp/mapper@1.txt'
    right_path = 'd:/tmp/mapper@2.txt'

    def __init__(self):
        pass

    def map(self):
        with open(self.left_path, 'r') as fin:
            lines = fin.readlines()
            for line in lines:
                m = re.match(r'.*class\s+(?P<class_name>\w+)', lines[0])
                if m:
                    class_name = m.group('class_name')
                    print 'internal static %s To %s {' % (class_name, class_name)
                    print ''
                else:
                    m = re.match(r'.*(?P<prop_name>\w+)', line)
                    if m:
                        prop_name = m.group('prop_name')
                        print '{}'


if __name__ == '__main__':
    Mapper().map()
