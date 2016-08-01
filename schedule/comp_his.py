# encoding: utf-8
# -*- coding: utf-8 -*-
from app import read_to_json


def main():
    h5_resp = read_to_json('6_.txt', 'd:/tmp')
    api_resp = read_to_json('7_.txt', 'd:/tmp')

    h5_ids = []
    api_ids = []
    for trip in h5_resp['orderInfo']:
        h5_ids.append(trip['tripId'])

    for trip in api_resp['UserActionList']:
        api_ids.append(trip['SmartTripID'])

    # print h5_ids
    # print api_ids
    print 'diff:'
    print 'only api:'
    print [item for item in api_ids if item not in h5_ids]

    print 'only h5'
    print [item for item in h5_ids if item not in api_ids]


if __name__ == '__main__':
    main()
