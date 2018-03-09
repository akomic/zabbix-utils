#!/usr/bin/env python3
import sys
import json
import logging
import argparse
from drivers.ec2 import EC2
from drivers.zabbix import Zabbix

import pprint

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Zabbix AWS Discovery')
parser.add_argument('-c', dest='configFile', default='./config.json',
                    help='Config file location (default ./config.json')
parser.add_argument('-l', dest='loglevel',
                    choices=[
                        'CRITICAL',
                        'ERROR',
                        'WARNING',
                        'INFO',
                        'DEBUG',
                        'NOTSET'
                    ],
                    default='INFO',
                    help='Loglevel')

args = parser.parse_args()

with open(args.configFile) as config_file:
    Config = json.load(config_file)

logger = logging.getLogger()
ch = logging.StreamHandler()
logLevel = logging.getLevelName(args.loglevel)
ch.setLevel(logLevel)
logger.addHandler(ch)


z = Zabbix(Config['Zabbix'])
zhosts = z.getHosts()

ec2 = EC2(Config['AWS'])
instances = ec2.getInstances()

for zhostName, zhost in zhosts.items():
    if zhostName not in instances:
        print("{} : DELETE".format(zhostName))
        z.deleteHost(zhost['hostid'])
