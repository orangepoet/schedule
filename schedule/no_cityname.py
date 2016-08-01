# encoding: utf-8
# -*- coding: utf-8 -*-
import re

from app import read_to_lines


def main():
    lines = read_to_lines('log.txt', 'd:/tmp')

    mutiple_id_set = []
    single_set = []
    for line in lines:
        line_strip = line.strip()
        matches = re.findall(pattern='\[([\d,]+)\]', string=line_strip)
        if len(matches) > 0:
            match = matches[0]
            if ',' in match:
                mutiple_id_set.append(match)
            else:
                single_set.append(match)

    print '''
SELECT *
FROM   SMARTTRIP WITH (NOLOCK)
WHERE  SMARTTRIPID IN ({0})
AND SUBTYPE<>2001
          '''.format(','.join(single_set))

    for item in mutiple_id_set:
        print'''
SELECT *
FROM   SMARTTRIP WITH (NOLOCK)
WHERE  SMARTTRIPID IN ({0})
AND SUBTYPE<>2001
        '''.format(item)

    print 'done'


if __name__ == '__main__':
    main()
