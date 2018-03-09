Zabbix AWS Discovery
=======================

# Installation

- Copy everything to /etc/zabbix/zabbix-aws-discovery/.

# Configuration
- Copy config.json to /etc/zabbix/zabbix-aws-discovery/config.json
- In AWS IAM create user with the following policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DevToolReadAll",
            "Action": [
                "ecs:ListClusters",
                "ecs:ListContainerInstances",
                "ecs:DescribeClusters",
                "ecs:DescribeContainerInstances",
                "ecs:ListServices",
                "ecs:DescribeServices",
                "ec2:DescribeInstances"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```
Use KEY and SECRET of this user in config.json.

- In Zabbix create user with privileges to list all hosts and edit them.
- Edit /etc/zabbix/zabbix-aws-discovery/config.json


NOTE: AWS section of config file supports multiple AWS accounts. User under which the script is going to be executed needs to have AWS_DEFAULT_PROFILE env variable set.

## EC2

### Create AutoDiscovery
On Zabbix under Configuration > Actions > Auto Registration, create AutoRegistration action which is adding all AWS EC2 instances under the same Host Group.
This group is going to be used to sync against AWS. If host is present in this Host Group but doesn't exist on AWS, it's going to be disabled on Zabbix.
Host name of each registered host has to be the same as EC2 instance name.

# Running
Add the following to crontab

```
*/5 * * * * /etc/zabbix/zabbix-aws-discovery/discovery.py -c /etc/zabbix/zabbix-aws-discovery/config.json
```
