# RabbitMQ Zabbix monitoring tools

Queries RabbitMQ API and caches results to speed things up.
It's using cache file locking to avoid race condition.

## Installation

### RabbitMQ
* Create user on RabbitMQ that can read virtualhosts you would like to monitor

### RabbitMQ Server

```shell
pip install -r requirements.txt
mkdir -p /etc/zabbix/scripts
```

* Copy userparameter_rabbitmq.conf to /etc/zabbix/zabbix_agentd.d
* Copy rabbitmq.py to /etc/zabbix/scripts/
* Edit /etc/zabbix/scripts/rabbitmq.py and enter host/user/pass
* Import zbx_export_templates.xml

```shell
chown zabbix. /etc/zabbix/scripts/rabbitmq.py
* systemctl restart zabbix-agent
```
