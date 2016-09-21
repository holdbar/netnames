import re
import os

# Path to dhcpd.leases

path = '/var/lib/dhcpd/dhcpd.leases'

# Utility lists

address_list = []  # List with lines of DHCP log
mac_name_list = []  # List of pairs MAC - Device name
arp_list = []  # List of pairs MAC - IP
temp_arp_list = []  # Temp list of info from ARP-tables
max_date_list = []  # List of pairs MAC - Device name with max date
temp_date_list = []  # Temp list for max date search
result_list = []  # Result list of current connections IP - Device name - MAC
index_list = []   # Utility list for definition of item index

# Regexp patterns

ip_pattern = r'[0-9]+(?:\.[0-9]+){3}'  # IP pattern
mac_pattern = r'[0-9a-f]+(?:\:[0-9a-f]+){5}'  # MAC pattern
date_pattern = r'\d+/\d+/\d+\s\d+\:\d+\:\d+'  # Datetime pattern
name_pattern = r'client-hostname.\"(.+)\"'  # Pattern of line with client-name
pure_name_pattern = r'\"(.+)\"'   # Pattern of client-name
arp_pattern = r'\(.+\n'  # Pattern of line in ARP-tables
dhcp_pattern = r'{[^}]+}'  # Pattern of block in dhcpd.leases

# Reading of the DHCP log

read_file = open(Path)
address_string = read_file.read()
read_file.close()

# Splitting of dhcpd.leases into blocks

address_list = re.findall(dhcp_pattern, address_string)

try:
    for item in address_list:
        if re.search(name_pattern, item):
            raw_name = re.search(name_pattern, item).group(0)
            name = re.search(pure_name_pattern, raw_name).group(0)
            date = re.search(date_pattern, item).group(0)
            mac = re.search(mac_pattern, item).group(0)
            mac_name_list.append([name, mac, date])
        else:
            name = "###NO NAME###"
            date = re.search(date_pattern, item).group(0)
            mac = re.search(mac_pattern, item).group(0)
            mac_name_list.append([name, mac, date])
except AttributeError:  # Exception will appear if there is no MAC in th block
    pass                # Such blocks are useless

# Sort by MAC


def sort_col(i):
    return i[1]

mac_name_list.sort(key=sort_col)

#Search of names with max date
#Sort by date


def sort_date(j):
    return j[2]


for x in range(len(mac_name_list)):
    if mac_name_list[x][0] == "###NO NAME###":  # Excluding info recieved from blocks without client-name
        pass
    elif mac_name_list[x][1] == mac_name_list[x+1][1]:  # If next item is indent to current
        temp_date_list.append(mac_name_list[x])         # we add current item to temp list
    elif mac_name_list[x][1] != mac_name_list[x+1][1]:  # If next item is not indent to current
        temp_date_list.append(mac_name_list[x])         # we add current item to temp list
        temp_date_list.sort(key=sort_date)              # list sorts by date
        temp_date_list.reverse()                        # list is reverted so max date is in list[0]
        max_date_list.append(temp_date_list[0])         # we add item with max date to result list
        temp_date_list.clear()                          # and clear temp list

# Recieving current info from ARP-tables

arp = os.popen('arp -a')
read_file = arp.read()
temp_arp_list = re.findall(arp_pattern, read_file)
arp.close()

# Processing of current data from ARP-tables

for item in temp_arp_list:
    if re.search(mac_pattern, item):
        mac_from_arp = re.search(mac_pattern, item).group(0)
        ip_address = re.search(ip_pattern, item).group(0)
    elif re.search(r'<incomplete>', item):
        mac_from_arp = "###NO MAC###"
        ip_address = re.search(ip_pattern, item).group(0)
    arp_list.append([ip_address, mac_from_arp])

# Processing of the results

for i in range(len(arp_list)):
    for j in range(len(max_date_list)):
        if arp_list[i][1] == max_date_list[j][1]:
            result_list.append([arp_list[i][0], max_date_list[j][0], max_date_list[j][1]])
            index_list.append(i)
    if arp_list[i][1] == '<incomplete>':
        result_list.append([arp_list[i][0], 'Unknown name', arp_list[i][1]])
        index_list.append(i)

for item in arp_list:
    if arp_list.index(item) in index_list:
        continue
    else:
        result_list.append(item)

# Writing down into the file for the further output

l = open('results', 'w')

for z in range(len(result_list)):
    if len(result_list[z]) < 3:
        tmp = "{} -- {} -- {}".format(result_list[z][0], 'Unknown name', result_list[z][1])
        l.write(str(tmp) + '\n')    
    else:
        tmp = "{} -- {} -- {}".format(result_list[z][0], result_list[z][1], result_list[z][2])
        l.write(str(tmp) + '\n')

l.close()

# This part can be removed if you'll use script as cgi to view output in browser

l = open('results', 'r')

for line in l:
    print(line)
l.close()
