#!/usr/bin/env python
import sys
import json
import argparse
import requests

parser = argparse.ArgumentParser(description='Zabbix Consul')

parser.add_argument('-s', dest='server_address', default='localhost',
                    help='Consul Server Address')
parser.add_argument('-p', dest='server_port', default='8500',
                    help='Consul Server Port')
parser.add_argument('-t', dest='server_token', default=None,
                    help='Consul Server Token')
parser.add_argument('-nn', dest='node_name',
                    help='Node Name')
parser.add_argument('-sn', dest='service_name',
                    help='Service Name')
parser.add_argument('-a', dest='action', required=True,
                    choices=[
                        'nodeDiscovery', 'nodeStatus',
                        'serviceDiscovery', 'serviceStatus'
                    ],
                    help='Action')
parser.add_argument('-d', dest='debug', action='store_true', default=False,
                    help='Debug')
args = parser.parse_args()


def fetch(url, ret={}):
    try:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            if args.debug:
                print(r.status_code, r.text)
                sys.exit(1)
            return ret
        return json.loads(r.text)

    except Exception as e:
        if args.debug:
            print(str(e))
            sys.exit(1)
        return ret

def nodeDiscovery(url):
    discovery_list = {}
    discovery_list['data'] = []


    nodes = fetch(url)

    for node in nodes:
        if node['Checks'][0]['CheckID'] == 'serfHealth':
            zbx_item = {
                "{#NODEID}": node['Node']['ID'],
                "{#NODENAME}": node['Node']['Node'],
                "{#NODEADDRESS}": node['Node']['Address'],
                "{#NODEDATACENTER}": node['Node']['Datacenter']
            }
            discovery_list['data'].append(zbx_item)
    print(json.dumps(discovery_list, indent=4, sort_keys=True))

def nodeStatus(url):
    node = fetch(url)

    try:
        status = 1 if node[0]['Status'] == 'passing' else 0 
        print(status)
    except Exception as e:
        if args.debug:
            print(str(e))
            sys.exit(1)
        print(0)

def serviceDiscovery(url):
    discovery_list = {}
    discovery_list['data'] = []


    services = fetch(url)

    for service in services:
        zbx_item = {
            "{#SERVICENAME}": service
        }
        discovery_list['data'].append(zbx_item)
    print(json.dumps(discovery_list, indent=4, sort_keys=True))

def serviceStatus(url):
    services = fetch(url)

    try:
        for service in services:
            if service['Checks'][0]['Status'] != 'passing':
                print(0)
                return

        print(1)
    except Exception as e:
        if args.debug:
            print(str(e))
            sys.exit(1)
        print(0)

headers = {}
if args.server_token:
    headers = {'X-Consul-Token': args.server_token}

if args.action == 'nodeDiscovery':
    nodeDiscovery("http://{}:{}/v1/health/service/consul".format(
        args.server_address,
        args.server_port
    ))
elif args.action == 'nodeStatus':
    if not args.node_name:
        print("-n <node_name> required")
        sys.exit(1)
    else:
        nodeStatus("http://{}:{}/v1/health/node/{}".format(
            args.server_address,
            args.server_port,
            args.node_name
        ))
elif args.action == 'serviceDiscovery':
    serviceDiscovery("http://{}:{}/v1/catalog/services".format(
        args.server_address,
        args.server_port
    ))
elif args.action == 'serviceStatus':
    if not args.service_name:
        print("-sn <service_name> required")
        sys.exit(1)
    else:
        serviceStatus("http://{}:{}/v1/health/service/{}".format(
            args.server_address,
            args.server_port,
            args.service_name
        ))
