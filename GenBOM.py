import xml.etree.ElementTree as ET
import re
import sys
import csv

import json
from collections import OrderedDict
import pprint
pp = pprint.PrettyPrinter(indent=4)


component = ".//comp"

desig_ptn = re.compile(r'[a-zA-Z][a-zA-Z]?')

def define_config():
    """ """
    with open("./conf.json", 'r') as conf:
        config = json.load(conf)[0]
        config['project']['bom_format'] = \
            config['BOM_formats'][config['project']['bom_format']]
        return config['project']

def extract_parts(xml_dir):
    """ """
    parts_list = []
    tree = ET.parse(xml_dir)
    root = tree.getroot()
    for comp in root.iter('comp'):
        part = {}
        part['ref'] = comp.attrib['ref']
        for field in comp.iter('field'):
            if field.text in 'value':
                part[field.attrib['name']] = None
            else:
                part[field.attrib['name']] = field.text
        parts_list.append(part)
    return parts_list

def bom_list_gen(parts_list, bom_format):
    """ """
    bom_list = []
    for part in parts_list:
        bom_line = bom_format
        if part['MPN'] not in bom_list[0:-1]['Manufacturer Part Number']:
            print("new")
        else:
            print("old")

def main():
    """  """
    project = define_config()
    xml_dir = project['dir'] + project['name'] + "/" + project['name'] + ".xml"
    
    bom_list_gen(extract_parts(xml_dir), project['bom_format'])
    


if __name__ == '__main__':
    main()