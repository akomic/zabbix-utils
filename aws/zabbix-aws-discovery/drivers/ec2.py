import boto3
import pprint

pp = pprint.PrettyPrinter(indent=4)


class EC2(object):
    def __init__(self, AWSAccounts):
        self.accounts = AWSAccounts
        self.ec2 = {}

        self.instances = []

        self.__login()

    def __login(self):
        for accountName in self.accounts:
            if 'key' not in self.accounts[accountName]:
                next
            if 'secret' not in self.accounts[accountName]:
                next

            self.ec2[accountName] = boto3.client(
                'ec2',
                aws_access_key_id=self.accounts[accountName]['key'],
                aws_secret_access_key=self.accounts[accountName]['secret']
            )

    def __parse_instance(self, instance):
        return instance['InstanceId']

    def getInstances(self):
        for accountName, ec2 in self.ec2.items():
            response = ec2.describe_instances()

            for reservation in response['Reservations']:
                for inst in reservation['Instances']:
                    if inst['State']['Name'] == 'running':
                        self.instances.append(self.__parse_instance(inst))

        return self.instances
