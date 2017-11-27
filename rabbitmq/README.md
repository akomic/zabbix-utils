# RabbitMQ Zabbix monitoring tools

Queries RabbitMQ API and caches results to speed things up.
It's using cache file locking to avoid race condition.

## Installation

### RabbitMQ
* Create user on RabbitMQ that can read virtualhosts you would like to monitor

### RabbitMQ Server

Clone this repo

```shell
cd zabbix-utils/rabbitmq
pip install -r requirements.txt
mkdir -p /etc/zabbix/scripts
cp rabbitmq.py /etc/zabbix/scripts/
chown zabbix. /etc/zabbix/scripts/rabbitmq.py
chmod 700 /etc/zabbix/scripts/rabbitmq.py
cp userparameter_rabbitmq.conf /etc/zabbix/zabbix_agentd.d/
```

* Edit /etc/zabbix/scripts/rabbitmq.py and enter host/user/pass
* Import zbx_export_templates.xml

```shell
systemctl restart zabbix-agent
```
