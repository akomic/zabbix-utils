import sys
import logging
from pyzabbix import ZabbixAPI

import pprint

pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger()


class Zabbix(object):
    def __init__(self, config):
        self.config = config
        self.data = {}

        self.__login()

    def __login(self):
        self.zapi = ZabbixAPI(self.config['URL'])
        self.zapi.session.verify = True
        self.zapi.timeout = 5
        self.zapi.login(self.config['User'], self.config['Pass'])

    def __hostInGroup(self, host, groupName):
        for g in host['groups']:
            if g['name'] == groupName:
                return True
        return False

    def __parse_host(self, host):
        # pp.pprint(host)
        self.data[host['host']] = {
            'name': host['name'],
            'hostid': host['hostid']
        }

    def __fetch(self):
        # try:
        hostsData = self.zapi.host.get(
            output='extend',
            selectGroups='extend'
        )
        for h in hostsData:
            if (
                self.__hostInGroup(h, 'AWSAutoRegistered') and
                h['status'] == '0'
            ):
                self.__parse_host(h)

    def disableHost(self, hostid):
        self.zapi.host.update(
            hostid=hostid,
            status='1'
        )

    def deleteHost(self, hostid):
        self.zapi.host.delete(hostid)

    def getHosts(self):
        self.__fetch()
        return self.data
