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

    ### Gets vManage variables from cookie and returns a vManage login object
    vmanage = rest_api_lib(vmanage_name, vmanage_user, vmanage_pass)

    return vmanage

def list_policy_tlocs(list_id = ''):

    vmanage = login()
    tlocs = vmanage.get_request(f'template/policy/list/tloc/{list_id}')
    vmanage.logout()
    return tlocs

def put_policy_tlocs(payload):

    vmanage = login()
    list_id = vmanage.post_request('template/policy/list/tloc',payload)
    vmanage.logout()
    return list_id

def read_list_file(listfile = 'list.csv'):

    file = open(listfile)
    payload = {}
    payload['name'] = file.readline().split(',')[1]
    payload['description'] = file.readline().split(',')[1]
    payload['type'] = file.readline().split(',')[1]
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

payload = read_list_file()
print(json.dumps(payload, indent=2))
list_id = put_policy_tlocs(payload)
print(list_id)
print(json.dumps(list_policy_tlocs(list_id['listId'])))