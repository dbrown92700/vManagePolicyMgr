#!/usr/bin/env python3
"""
Copyright (c) 2012 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
__author__ = "David Brown <davibrow@cisco.com>"
__contributors__ = []
__copyright__ = "Copyright (c) 2012 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from includes import *
from vmanage_api import rest_api_lib
import json

def login():

    vmanage = rest_api_lib(vmanage_name, vmanage_user, vmanage_pass)
    return vmanage

def read_list_file(listfile = 'list.csv'):

    file = open(listfile)
    payload = {}
    payload['name'] = file.readline().split(',')[1].rstrip('\n')
    payload['description'] = file.readline().split(',')[1].rstrip('\n')
    payload['type'] = file.readline().split(',')[1].rstrip('\n')
    header = file.readline().split(',')
    entries = []
    for line in file.readlines():
        linelist = line.split(',')
        entry = {}
        for item in header:
            entry[item.rstrip('\n')] = linelist.pop(0).rstrip('\n')
        entries.append(entry)
    payload['entries'] = entries
    payload['owner'] = vmanage_user
    payload['readOnly'] = False
    payload['version'] = '0'
    payload['infoTag'] = ''

    return payload

if __name__ == '__main__':

    # Read in list file

    filename = input("Input filename: ").rstrip('.csv') + '.csv'
    payload = read_list_file(filename)
    print(json.dumps(payload, indent=2))

    # Set the right REST call URLs based on the type of list

    if payload['type'] == 'tloc':
        geturl = 'template/policy/list/tloc'
        posturl = 'template/policy/list/tloc'
    elif payload['type'] == 'dataPrefix':
        geturl = 'template/policy/list/dataprefix'
        posturl = 'template/policy/list/dataprefix'

    # POST the list to vManage and GET the list to verify

    print(payload['type'])

    vmanage = login()
    list_id = vmanage.post_request(posturl, payload)['listId']
    # list_id = put_policy_tlocs(payload)
    print(list_id)
    read_list = vmanage.get_request(f'{geturl}/{list_id}')
    print(json.dumps(read_list, indent=2))
    vmanage.logout()