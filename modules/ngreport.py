#!/usr/bin/env python
import sys
import os
import subprocess

import nginit
from nglog import log

def report_mysql(host,user,passwd,database,table,data):
    """
    report collect data to mysql .
    need MySQL-python module
    note that:
        host is your mysql server ip or hostname
        user is your mysql user
        passwd is your mysql password
        database is the database store collect data
        data is a dict (note:is dict),the key is mysql table's key ,and the
            value of the dict is your collect data or other thing 
    """
    try:
        import MySQLdb
    except ImportError:
        log.error('MySQLdb module is not install in this server !')
        sys.exit(200)
    sql = 'insert into `' + table + '` ('
    keys = []
    values = []
    
    try:
        conn = MySQLdb.connect(host,user,passwd)
        conn.select_db(database)
        cursor = conn.cursor()
    except:
        log.error('connect mysql server or database  error !')
    if isinstance(data,dict):
        for (key,value) in data.items():
           keys.append(key)
           values.append(value)
        for i in range(len(keys)):
            if i < len(keys) - 1 :
                sql += '`' + str(keys[i]) + '`'  + ','
            else:
                sql += '`' + str(keys[i]) + '`  ) values ('
        for j in range(len(values)):
            if j < len(values) - 1:
                 sql += '"' + str(values[j]) + '"'  + ','
            else:
                 sql += '"' + str(values[j]) + '" )' 
    else:
        log.error(' input data not a dict')

    try:        
        cursor.execute(sql)
        conn.commit()
        log.info('report ' + str(data) + ' to ' + host + ' success')
    except:
        log.error('insert sql '+ sql +' error')
def report_mongo():
    """
    report collect data to mongodb
    """


def report_redis():
    """
    report collect data to redis
    """


def report_memcache():
    """
    report collect data to memcache
    """

def report_http_post():
    """
    report collect data use http post
    """

if __name__ == '__main__':
    data = {'hostname':'chenqing.org','load':15}
    host = nginit.MYSQL_HOST
    user = nginit.MYSQL_USER
    passwd = nginit.MYSQL_PASSWD
    database = nginit.MYSQL_DATABASE
    #report_mysql(host,user,passwd,database,'test',data)
