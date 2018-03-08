#!/usr/bin/python
from datetime import datetime
from netaddr import IPNetwork
import time
import sys
import os

datestring = datetime.strftime(datetime.now(), '%Y%m%d')
input_file = sys.argv[1]

# subnets to ignore
ignore_subnets = ['/4', '/8', '/10', '/12', '0.0.0.0/8', '10.0.0.0/8', '127.0.0.0/8', '240.0.0.0/4', '100.64.0.0/10', '172.16.0.0/12']

# custom ips to ignore
ignore_custom_ips = [ ]

# start time tracking
start = time.time()    

# read Ingest file, remove ignored subnets, write to tmp file
full_list = open(input_file, 'r')
filtered_list = open('filtered_list-'+datestring+'.tmp', 'a')

for line in full_list:
  if not any (ignore_subnet in line for ignore_subnet in ignore_subnets):
    filtered_list.write(line)

full_list.close()
filtered_list.close()

# read tmp file, expand subnets, write to second tmp file
filtered_list = open('filtered_list-'+datestring+'.tmp', 'r+')
expanded_list = open('expanded_list-'+datestring+'.txt', 'a')

for line in filtered_list:
  subnet = IPNetwork(line)
  for ip in IPNetwork(subnet):
    ips = str(ip)
    if ips not in ignore_custom_ips:
      expanded_list.write(ips + '\n')    

os.remove(filtered_list.name)
filtered_list.close()

# read second tmp file, transform list for redis
#expanded_list = open('expanded_list-'+datestring+'.tmp', 'r+')
#redis_list = open('redis_ip_list-'+datestring+'.txt', 'a')

#for line in expanded_list:
#    length = str(len(line) - 1)
#    redis_transform = ('*3\r\n$3\r\nSET\r\n$' + length + '\r\n' + line + '$1\r\n1\r\n*3\r\n$6\r\nEXPIRE\r\n$' + length + '\r\n' + line + '$5\r\n86400')
#    redis_list.write(redis_transform + '\n')

#os.remove(expanded_list.name)

# end time tracking, caclulate total
end = time.time()
total = end - start

print ('Ingest complete in: %s seconds. File to transform to redis:  %s' % (total, expanded_list.name)) 

