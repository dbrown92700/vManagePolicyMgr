#!/usr/bin/env python3
'''
    This module is still in development.
    Intent is to parse and convert the CLI output of a vSmart policy.
'''

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

import sys, yaml, json

action_sections = ['match', 'set', 'action', 'sequence']
policy_elements = {'sla-class': 'SC',\
                   'data-policy': 'DP',\
                   'data-prefix-list': 'DPL',\
                   'prefix-list': 'PL',\
                   'tloc-list': 'TL',\
                   'app-list': 'AL',\
                   'color-list': 'CL',\
                   'site-list': 'SL',\
                   'control-policy': 'CP',\
                   'app-route-policy': 'ARP',\
                   'cflowd-template': 'CT',
                   'vpn-list': 'VL'}

def list_elements(filename):

    # Prints only the top level lines of each policy element

    outfile = open('vsmartpolicy-toplines.txt', 'w')
    with open(filename) as file:
        config = file.readlines()
        for index, line in enumerate(config):
            if not (line[1] in ['', ' ', '!', '\n']):
                line = line.rstrip('\n')
                print(f'{index:10}:{line}')
                outfile.write(f'{index:10}:{line}\n')
    outfile.close()

def list_single(filename):

    # Prints only lines with single keywords

    outfile = open('vsmartpolicy-singleitems.txt', 'w')
    with open(filename) as file:
        config = file.readlines()
        for index, line in enumerate(config):
            line = ' '.join(line.lstrip(' ').split())
            if line.count(' ') == 0 and line != '!':
                line = line.rstrip('\n')
                print(f'{index:10}:{line}')
                outfile.write(f'{index:10}:{line}\n')
        outfile.close()


def list_multi(filename):

    # print lines with multiple settings

    outfile = open('policy-multilines.txt', 'w')
    with open(filename) as file:
        config = file.readlines()
        for index, line in enumerate(config):
            line = ' '.join(line.lstrip(' ').split())
            if line.count(' ') > 1:
                line = line.rstrip('\n')
                print(f'{index:10}:{line}')
                outfile.write(f'{index:10}:{line}\n')
    outfile.close()

def policy_to_html(filename):

    # Finding all the sections

    # Read the config into a list "config"

    outfile = open('vsmartpolicy.html', 'w')
    file = open(filename)
    config = file.readlines()
    file.close()

    #
    # Parse the file for all section elements and put them in a list
    #

    elements = {}

    for lineNum, line in enumerate(config):
        if line == 'apply-policy\n':
            break
        if not ('!' in line):   # Skip lines with !

            # calculate the indent on this line vs. the next line
            leader = line.count(' ') - line.lstrip(' ').count(' ')
            nextline = config[lineNum + 1]
            leadernext = nextline.count(' ') - nextline.lstrip(' ').count(' ')

            # Track if we're parsing the lists section of the config
            if leader == 1:
                if line == ' lists\n':
                    lists_section = True
                else:
                    lists_section = False

            if leadernext > leader: # This is a section line
                if ' ' in line.lstrip(' '):  # This has a name
                    lineSplit = line.lstrip(' ').rstrip('\n').split()
                    if (lineSplit[0] in action_sections) or ((not lists_section) and (lineSplit[0] == 'vpn-list')):
                        pass
                    else:
                        if not lineSplit[0] in elements:
                            elements[lineSplit[0]] = []
                        elements[lineSplit[0]].append(lineSplit[1])
                        config[lineNum] = leader * ' ' + \
                                          f'{lineSplit[0]} <a id="{policy_elements[lineSplit[0]]}:{lineSplit[1]}"><b>{lineSplit[1]}'\
                                          + '</b></a>'

    #
    # Parse the file and link all references to the elements in the list
    #

    apply_section = False
    for lineNum, line in enumerate(config):
        if line == 'apply-policy\n':
            apply_section = True

        if line == ' lists\n':
            lists_section = True
        else:
            lists_section = False

        if not ('!' in line):   # Skip lines with !
            leader = line.count(' ') - line.lstrip(' ').count(' ')
            nextline = config[lineNum + 1]
            leadernext = nextline.count(' ') - nextline.lstrip(' ').count(' ')
            lineSplit = line.lstrip(' ').rstrip('\n').split()
            if (not (leadernext > leader)) or apply_section or ((not lists_section) and (lineSplit[0] == 'vpn-list')): # This is a config element
                for index, keyword in enumerate(lineSplit):
                    for element_type, instances in elements.items():
                        if keyword in instances:
                            if element_type in lineSplit[index - 1]:
                                lineSplit[
                                    index] = f'<a href="#{policy_elements[element_type]}:{keyword}">{keyword}' + '</a>'
                                break
                config[lineNum] = leader * ' ' + ' '.join(lineSplit)

    #
    # Create Web Page Policy
    #

    outfile.write('<html><body>\n<h1>Policy Elements</h1>\n')

    # Create table of contents for policy elements
    for element_type, instances in elements.items():
        outfile.write(f'<h2>{element_type}'+'</h2>\n')
        for line in instances:
            outfile.write(f'<a href="#{policy_elements[element_type]}:{line}">{line}</a><br>\n')

    # Write the policy
    outfile.write('<h1>Policy</h1>\n')
    for index, line in enumerate(config):
        leader = line.count(' ') - line.lstrip(' ').count(' ')
        line = leader * '&nbsp;' * 3 + line.lstrip(' ')
        # line = leader * ' ' * 3 + line.lstrip(' ')
        outfile.write(f'{index}:{line}'+'<br>\n')
    outfile.write('</html></body>')
    outfile.close()

    return elements

def convert_to_yaml(filename):

    # Trying to convert a vSmart CLI policy into YAML format

    yamltext = ''
    with open(filename) as file:
        config = file.readlines()
        for lineNum, line in enumerate(config):
            if not ('!' in line):   # Skip lines with !

                # calculate the indent on this line vs. the next line
                leader = line.count(' ') - line.lstrip(' ').count(' ')
                nextline = config[lineNum + 1]
                leadernext = nextline.count(' ') - nextline.lstrip(' ').count(' ')
                if leadernext > leader:  # This is a section line
                    if ' ' in line.lstrip(' '):
                        lineSplit = line.lstrip(' ').rstrip('\n').split()

                        yamlline = ' ' * leader + lineSplit[0] + ':\n'
                        yamlline += ' ' * leader + f' name: {lineSplit[1]}'
                    else:
                        yamlline = line.replace('\n', ':')
                else:  # This is a setting line

                    if ' ' in line.lstrip(' '):  # see if there is a ' ' in the line indicating a keyword and setting
                        yamlline = ' ' * leader + ': '.join(line.lstrip(' ').split()).rstrip('\n')
                    else:
                        yamlline = ' ' * leader + 'setting: ' + line.lstrip(' ').rstrip('\n')
                yamltext += yamlline + '\n'
    return yamltext


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = 'vsmartpolicy.txt'

    #print(list_single(file))

    elements = policy_to_html(file)

    print(elements)
