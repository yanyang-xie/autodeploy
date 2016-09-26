#!/usr/bin/python
# coding:utf-8
# author: yanyang.xie

TOMCAT_SERVICE = 'tomcat'
MEMCACHED_SERVICE = 'memcached'
ZOOKEEPER_SERVICE = 'zookeeper'
REDIS_SERVICE = 'redis'

TOMCAT_DIR = '/usr/local/thistech/tomcat'

SPARK_COMMAND_START = 'su spark -c "sh /usr/local/spark/sbin/start-thistech.sh"'
SPARK_COMMAND_STOP = 'su spark -c "sh /usr/local/spark/sbin/stop-all.sh"'


