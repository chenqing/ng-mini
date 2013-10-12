#!/usr/bin/env python
#coding=utf-8
import os
import sys
import ConfigParser
import subprocess
from ngsubprocess import get_output

'''
check python version,if version lt 2.5,mini-ng will not be run
'''
py   = sys.version_info
py25 = py <  (2, 5, 0)
if py25:
    print 'python version is need great than 2.5'
    sys.exit(3)
PY_PATH=''
if subprocess.call('which python2.7 >/dev/null 2>&1 || which python27 >/dev/null 2>&1',shell=True) == 0:
    PY_PATH = get_output('which python2.7 2>/dev/null || which python27')
elif subprocess.call('which python2.6 >/dev/null 2>&1 || which python26 >/dev/null 2>&1',shell=True) == 0:
    PY_PATH = get_output('which python2.6 2>/dev/null || which python26 2>/dev/null')
PY_PATH = PY_PATH.replace('\n','')
'''
    定义程序的名称，版本，更新日期，作者信息
'''
APP_NAME = 'ng-mini'
APP_VERSION = 0.1
APP_AUTHOR = 'qing.chen'

'''
    处理程序的路径,可能需要手动更改
'''
APP_PATH = '/data/ng-mini'
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
    LOG_LEVEL = 'INFO'
#rrdtool 文件放在了哪里
try:
    RRDTOOL_PATH = cf.get('base','rrdtool_path')
except:
    RRDTOOL_PATH = get_output('/usr/bin/which rrdtool')

if not os.path.isfile(RRDTOOL_PATH):
    RRDTOOL_PATH = get_output('/usr/bin/which rrdtool')

RRDTOOL_PATH = RRDTOOL_PATH.replace('\n','')


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
    RRD_PATH = APP_PATH + '/' + 'rrd'

#font 字体文件路径
try:
    FONT_PATH = os.path.join(APP_PATH,'font')
except:
    FONT_PATH = APP_PATH + '/' + 'font'

#图片文件存放路径

try:
    PIC_PATH = os.path.join(APP_PATH,cf.get('base','graph_path'))
except:
    PIC_PATH = APP_PATH + '/' + 'web/pic/rrd'

#apps 自定义数据获取脚本的路径
try:
    APPS_PATH = os.path.join(APP_PATH,cf.get('base','apps_path'))
except:
    APPS_PATH = APP_PATH + '/' + 'apps'

#mysql database config
try:
    MYSQL_HOST=cf.get('mysql','host')
    MYSQL_USER=cf.get('mysql','user')
    MYSQL_PASSWD=cf.get('mysql','passwd')
    MYSQL_DATABASE=cf.get('mysql','database')
except:
    MYSQL_HOST=''
    MYSQL_USER=''
#mongodb database config
try:
    MONGO_HOST=cf.get('mongodb','host')
    MONGO_USER=cf.get('mongodb','user')
    MONGO_PORT=int(cf.get('mongodb','port'))
    MONGO_PASSWD=cf.get('mongodb','passwd')
    MONGO_DATABASE=cf.get('mongodb','database')
except:
    MONGO_HOST=''
    MONGO_USER=''
