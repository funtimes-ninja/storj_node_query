#!/usr/bin/env python3

"""
This script uses the linux command curl in a python subprocess to get the node
data from the stroj bridge api.
"""

import subprocess
import datetime
import pytz
from helper import Color

SITE = 'https://api.storj.io/contacts/'


def get_nodes(node_file):
    """ Read nodes from a text file into a list """
    with open(node_file) as file_node:
        nodes = file_node.readlines()
    final = [node.strip() for node in nodes[1:]]
    return final


def convert_time(time_str):
    """ Covert UTC timestamp into EST """
    t_format = "%Y-%m-%dT%H:%M:%S"
    date = datetime.datetime.strptime(time_str, t_format)
    date.strftime("%a %b %d %H:%M:%S")
    utc = pytz.timezone('UTC')
    aware_date = utc.localize(date)
    eastern = pytz.timezone('US/Eastern')
    eastern_date = aware_date.astimezone(eastern)
    converted = eastern_date.strftime("%Y-%m-%d %H:%M:%S")
    return converted


def compare_date(time_str):
    """ Compare date within 24 hours """
    t_format = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.now()-datetime.timedelta(hours=24) <= \
        datetime.datetime.strptime(time_str, t_format)


def compare_time(time_str):
    """ Compare timestamp at various hours """
    t_format = "%Y-%m-%d %H:%M:%S"
    if datetime.datetime.now()-datetime.timedelta(hours=3) <= \
       datetime.datetime.strptime(time_str, t_format):
        return 3
    elif datetime.datetime.now()-datetime.timedelta(hours=6) <= \
            datetime.datetime.strptime(time_str, t_format):
        return 6
    elif datetime.datetime.now()-datetime.timedelta(hours=12) <= \
            datetime.datetime.strptime(time_str, t_format):
        return 12
    elif datetime.datetime.now()-datetime.timedelta(hours=24) <= \
            datetime.datetime.strptime(time_str, t_format):
        return 24
    # Else catch all
    return 100


def proc_data(data):
    """ Process and convert the data and return a dict of the stored data """
    data_dict = {}
    for item, _ in enumerate(data):
        if 'lastSeen' in data[item]:
            time_stamp = data[item].split(':', 1)[1].split('.')[0]
            time_stamp = convert_time(time_stamp)
            data_dict['time_stamp'] = time_stamp
        if 'port' in data[item]:
            port = data[item].split(':')[1]
            data_dict['port'] = port
        if 'address' in data[item]:
            ip_addr = data[item].split(':')[1]
            data_dict['address'] = ip_addr
        if 'responseTime' in data[item]:
            resp_time = data[item].split(':')[1]
            data_dict['response'] = resp_time
        if 'reputation' in data[item]:
            rep = data[item].split(':')[1]
            data_dict['rep'] = rep
        if 'lastTimeout' in data[item]:
            timeout = data[item].split(':', 1)[1].split('.')[0]
            timeout = convert_time(timeout)
            data_dict['timeout'] = timeout
        if 'timeoutRate' in data[item]:
            time_rate = data[item].split(':')[1]
            data_dict['out_rate'] = time_rate
        if 'nodeID' in data[item]:
            node_id = data[item].split(':')[1]
            data_dict['nodeid'] = node_id
    return data_dict


def print_format(data):
    """ Format the and print the data to our liking """
    print("{:<40s}".format(data['nodeid']), end="")
    if compare_time(data['time_stamp']) == 3:
        Color.green(" {:<19s}".format(data['time_stamp']), end="")
    elif compare_time(data['time_stamp']) == 6:
        Color.yellow(" {:<19s}".format(data['time_stamp']), end="")
    else:
        Color.red(" {:<19s}".format(data['time_stamp']), end="")
    print(" {:<4s} ".format(data['rep']), end="")
    print(" {:<19s} ".format(data['response']), end="")
    try:
        if compare_date(data['timeout']):
            Color.red(" {:<19s}".format(data['timeout']))
        else:
            Color.white(" {:<19s}".format(data['timeout']))
    except KeyError:
        Color.green(" {:<19s}".format('None'))


def main():
    """ Main logic of the program """
    print("{:<40s} {:<19s} {:<5s} {:<20s} {:<20s}"
          .format('NODE ID', 'LAST CONTACT', 'REP', 'RESPONSE TIME',
                  'TIMEOUT'))
    nodes = get_nodes('./nodes.txt')
    for count, _ in enumerate(nodes):
        process = subprocess.check_output(['curl', '-s', SITE+nodes[count]],
                                          universal_newlines=True).strip()
        data = process.replace('{', '').replace('}', '').replace('"', '')\
                      .split(',')
        data = proc_data(data)
        print_format(data)


if __name__ == "__main__":
    main()
