import xml.etree.ElementTree as ET
import re
import csv
import json

component = ".//comp"
desig_ptn = re.compile(r'[a-zA-Z][a-zA-Z]?')


def define_config():
    """ """
    with open("./conf.json", 'r') as conf:
        config = json.load(conf)[0]
        config['project']['bom'] = \
            config['BOM'][config['project']['bom']]
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
            if field.text in 'n':
                part[field.attrib['name']] = None
            else:
                part[field.attrib['name']] = field.text
        parts_list.append(part)
    return parts_list


def gen_unite_list(parts_list, project):
    """"""
    mapping = project['bom']['mapping']
    comp_list = []
    unite_list = []
    for part in parts_list:
        comp_part = \
            {v[0]: part[v[1]] for v in mapping.items() if v[1] is not None}
        if comp_part not in comp_list:
            unite_list.append([comp_part, [part['ref']], 1])
            comp_list.append(comp_part)
        else:
            num = comp_list.index(comp_part)
            unite_list[num][1].append(part['ref'])
            unite_list[num][2] += 1
    return unite_list


def modify_line(unite_line):
    """ """
    sorted(unite_line[1], key=lambda x: int(desig_ptn.split(x)[1]))
    unite_line[0]['Designator'] = ','.join(unite_line[1])
    unite_line[0]['Quantity'] = unite_line[2]
    mod_line = unite_line[0]
    return [desig_ptn.match(unite_line[1][0]).group(), mod_line]


def gen_bom_list(mod_list):
    mod_list.sort(key=lambda desig: desig[0])
    return [bom_line[1] for bom_line in mod_list]


def main():
    """  """    
    project = define_config()
    prj_dir = project['dir'] + project['name'] + "/"
    rows = extract_parts(prj_dir + project['name'] + ".xml")
    mod_list = [modify_line(i) for i in gen_unite_list(rows, project)]


    with open(prj_dir + project['name'] + "-BOM" + ".csv", 'w', newline='\n') as ds:
        writer = csv.DictWriter(ds, project['bom']['column'])
        writer.writeheader()
        for row in gen_bom_list(mod_list):
            writer.writerow(row)


if __name__ == '__main__':
    main() 