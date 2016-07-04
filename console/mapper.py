# encoding: utf-8
# -*- coding: utf-8 -*-

def comp(n1, n2, t1, t2):
    if n1 == n2:
        return True
    elif n1 in n2 or n2 in n1:
        return True
    else:
        return False


def mapper(types):
    assert len(types) == 2
    for n1, t1 in types[0].iteritems():
        for n2, t2 in type[1].iteritems():
            if comp(n1, n2, t1, t2):
                print "{p1} = x.{p2},"


def main():
    from os.path import join, abspath
    import re

    types = []
    with open(join(abspath('..'), 'static/in/mapper.txt'), 'r') as fp:
        for line in fp.readlines():
            if 'class' in line:
                cs_type = dict()
                types.append(cs_type)
                if len(types) == 2:
                    break
            else:
                match = re.match(r'.*public\s+(?P<prop_type>\w+)\s+(?P<prop_name>\w+)\s+', line)
                if match:
                    cs_type[match.group('prop_name')] = match.group('prop_type')

    mapper(types)


if __name__ == '__main__':
    main()
