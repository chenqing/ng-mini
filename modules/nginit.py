#!/usr/bin/env python
#coding=utf-8
import os
import ConfigParser
from ngsubprocess import get_output


'''
    定义程序的名称，版本，更新日期，作者信息
'''
APP_NAME = 'ng-mini'
APP_VERSION = 0.1
APP_AUTHOR = 'qing.chen'

'''
    处理程序的路径,可能需要手动更改
'''
APP_PATH = '/Users/chenqing/hellopy/ng-mini'
#APP_PATH = os.path.abspath('.')

CONFIG_PATH = os.path.join(APP_PATH ,'etc')
'''
    配置文件解析
'''
cf = ConfigParser.ConfigParser()
cf.read(CONFIG_PATH + '/ng.conf')
#是不是要记录日志
LOGED = cf.get('log','log')
#日志的记录路径是什么，默认在程序目录下的log目录
try:
    LOG_PATH = cf.get('log','logpath')
except:
    LOG_PATH = APP_PATH + '/log/ng.log'

#日志级别
try:
    LOG_LEVEL = cf.get('log','log_level').upper()
except:
    LOG_LEVEL = 'WARNING'
#rrdtool 文件放在了哪里
try:
    RRDTOOL_PATH = cf.get('base','rrdtool_path')
    if not os.path.isdir(RRDTOOL_PATH):
        RRDTOOL_PATH = get_output('/usr/bin/which rrdtool')
except:
    try:
        RRDTOOL_PATH = get_output('/usr/bin/which rrdtool')
    except:
        RRDTOOL_PATH = ' '

#pid文件
try:
    PID = cf.get('base','pid')
except:
    PID = '/var/run/ng.pid'
#yaml文件的路径
try:
    YAML_PATH = CONFIG_PATH + '/' + cf.get('base','yaml_path')
except:
    YAML_PATH = ' '

#需要作图的app
try:
    APPS = cf.get('apps','enabled').split(' ')
except:
    APPS = ['base']

#rrd 文件路径

try:
    RRD_PATH = os.path.join(APP_PATH,cf.get('base','rrd_path'))
except:
    RRD_PATH = ' '


