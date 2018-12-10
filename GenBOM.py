import xml.etree.ElementTree as ET
import re
import sys
import csv

kc_pjname = "STR-X-Avionics"

kc_xmldir = "./" + kc_pjname + "/" + kc_pjname + ".xml"
component = ".//comp"

desig_ptn = re.compile(r'[a-zA-Z][a-zA-Z]?')
field_name = ['Desig', 'MPN', 'Agency']
header_name = ['Designator', 'Manufacturer Part Number', 'Quantity', 'Agency']


def combine(fd_key, fd_value):
    """  """
    field_dict = {}
    field_dict[field_name[0]] = fd_key
    field_dict.update(fd_value)
    return field_dict


def keyfunc(desig):
    return int(desig_ptn.split(desig)[1])


def main():
    """  """
    tree = ET.parse(kc_xmldir)
    root = tree.getroot()
    rows = {}

    field_extract = [
        combine(desig_raw.get("ref"), {
            field.get('name'): field.text
            for field in root.findall(
                component + "[@ref=\'" + desig_raw.get("ref") + "\']/fields/*"
            )
            if field.get('name') in field_name
        })
        for desig_raw in root.findall(component)
    ]
    for field_fact in field_extract:
        if field_fact[field_name[1]] not in rows:
            rows[field_fact[field_name[1]]] = {
                'Designator': [],
                'Manufacturer Part Number': None,
                'Quantity': None,
                'Agency': None
            }
        rows[field_fact[field_name[1]]][
            header_name[0]].append(field_fact[field_name[0]])
        rows[field_fact[field_name[1]]][
            header_name[1]] = field_fact[field_name[1]]
        rows[field_fact[field_name[1]]][
            header_name[2]] = len(rows[field_fact[field_name[1]]][header_name[0]])
        rows[field_fact[field_name[1]]][
            header_name[3]] = field_fact[field_name[2]]
    for npm, ls in rows.items():
        rows[npm][header_name[0]] = ','.join(
            sorted(rows[npm][header_name[0]],key=lambda x:keyfunc(x))
        )
    with open('test.csv', 'w', newline='\n') as ds:
        writer = csv.DictWriter(ds, header_name)
        writer.writeheader()
        for row in rows.values():
            # print(row['Agency'])
            if row['Agency'] == 'Digikey' or 'Mouser':
                # print("OK")
                writer.writerow(row)
            else:
                print("NG")

if __name__ == '__main__':
    main()