"""Render 'dmidecode' commend output into a proper format."""
from pprint import pprint

sample = """Getting SMBIOS data from sysfs.
SMBIOS 2.6 present.

Handle 0x0000, DMI type 0, 24 bytes
BIOS Information
        Vendor: LENOVO
        Version: 29CN40WW(V2.17)
        Release Date: 04/13/2011
        ROM Size: 2048 kB
        Characteristics:
                PCI is supported
                BIOS is upgradeable
                BIOS shadowing is allowed
                Boot from CD is supported
                Selectable boot is supported
                EDD is supported
                Japanese floppy for NEC 9800 1.2 MB is supported (int 13h)
                Japanese floppy for Toshiba 1.2 MB is supported (int 13h)
                5.25"/360 kB floppy services are supported (int 13h)
                5.25"/1.2 MB floppy services are supported (int 13h)
                3.5"/720 kB floppy services are supported (int 13h)
                3.5"/2.88 MB floppy services are supported (int 13h)
                8042 keyboard services are supported (int 9h)
                CGA/mono video services are supported (int 10h)
                ACPI is supported
                USB legacy is supported
                BIOS boot specification is supported
                Targeted content distribution is supported
        BIOS Revision: 1.40"""

def read_file(sample_file):
    all_lines = []
    text = sample_file.splitlines()
    for line in text:
        if line != "":
            all_lines.append(line)
    for line in all_lines:
        if line.startswith('Handle') :
            index = all_lines.index(line)
    lines = all_lines[index:]
    return lines

#pprint(read_file(sample))


def get_indent_level(line):
    ctr = 0
    for char in line:
        if char == " ":
            ctr +=1
        else:
            break
    return ctr

#print (get_indent_level('  hello')) #expect 2


def parse(lines):
    dmi_dict = {}
    keyvalue = {}
    property_list = []
    last_property = ''

    for line in lines:

        if line.startswith('Handle') :
            section = ''
            section = lines[lines.index(line)+1].strip()

        elif ':' in line:
            if line.split(':')[1] != '' :
                keyvalue.update({line.strip().split(':')[0] : line.strip().split(':')[1]})
            else :
                last_property = line.strip().split(':')[0]

        elif get_indent_level(line) >= get_indent_level(lines[lines.index(line)+1]):
            property_list.append(line.strip())

    keyvalue.update({last_property : property_list})
    dmi_dict[section] = keyvalue
    return dmi_dict

#pprint(parse(read_file(sample)))
