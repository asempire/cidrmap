#!/usr/bin/python3

import sys
import re
import ipaddress

# A small script to expand CIDR IPV4 notation to individual IPs, cuz why not...
if len(sys.argv) != 2:
    print(f"usage:{sys.argv[0]} IPV4/network_bitness")
    sys.exit(1)


def is_ipv4_cidr(ip):
    ip_reg = r'^(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})$'
    return re.match(ip_reg,sys.argv[1]) is not None

if is_ipv4_cidr(sys.argv[1]):
    
    netmask = sys.argv[1].split("/")
    if int(netmask[1]) > 32 or int(netmask[1]) < 0:
        print("please provide a valid IPV4 network address")
        sys.exit(1)
    octets = netmask[0].split(".")
    for octet in octets:
        if int(octet) > 255 or int(octet) < 0:
            print("please provide a valid IPV4 network address")
            sys.exit(1)
else:
    print("please provide a valid IPV4 network address")
    sys.exit(1)

cidr_range = sys.argv[1]

cidr_range = ipaddress.IPv4Network(cidr_range)

for ip in cidr_range:
    print(ip)