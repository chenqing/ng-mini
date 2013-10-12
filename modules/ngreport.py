#!/usr/bin/env python
import sys
import os
import subprocess

import nginit
from nglog import log

def report_mysql(data):
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
        conn = MySQLdb.connect(nginit.MYSQL_HOST,nginit.MYSQL_USER,nginit.MYSQL_PASSWD)
        conn.select_db(nginit.MYSQL_DATABASE)
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
def report_mongo(data):
    """
    report collect data to mongodb
    need pymongo library
    """
    try:
        import pymongo
    except:
        log.error('pymongo library is not installed in this server')
    #connect your mongo server
    conn = pymongo.MongoClient(host=str(nginit.MONGO_HOST))
    #get or create a new database
    db = conn.ng_mini
    #check auth
    db.authenticate(nginit.MONGO_USER,nginit.MONGO_PASSWD)
    #select a collecton (a table),assume your collection name is monitor
    collection = db.monitor
    if isinstance(data,dict):
        try:
            collection.insert(data)
            log.info('report ' + str(data) + 'to' + nginit.MONGO_HOST + ' success')
        except:
            log.error('report ' + str(data) + 'to' + nginit.MONGO_HOST + ' failed')
    else:
        log.error('data not a dict !')


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
    data = {'hostname':'chenqing.org','load':16}
    #report_mysql(host,user,passwd,database,'test',data)
    report_mongo(data)
