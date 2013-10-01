#!/usr/bin/env python
#coding:utf-8
#import pyrrd //考虑到通用性还是使用封装命令行的方法吧
import subprocess
import os
import time
import nginit
from nglog import log
from ngyaml import ngyaml

rrdtool = nginit.RRDTOOL_PATH

def create(filename,rrd_ds,rrd_dst,interval):
    '''
    rrdtool create in python
    '''
    start = int(time.time()) - 86400
    step = interval * 60
    cmd = "%s  create %s \
    --start %s --step %s \
    DS:%s:%s:600:0:U  \
    RRA:LAST:0.5:1:600 RRA:LAST:0.5:6:700 RRA:LAST:0.5:24:775 RRA:LAST:0.5:288:797 \
    RRA:AVERAGE:0.5:1:600 RRA:AVERAGE:0.5:6:700 RRA:AVERAGE:0.5:24:775 RRA:AVERAGE:0.5:288:797\
    RRA:MAX:0.5:1:600 RRA:MAX:0.5:6:700 RRA:MAX:0.5:24:775 RRA:MAX:0.5:444:797 \
    RRA:MIN:0.5:1:600 RRA:MIN:0.5:6:700 RRA:MIN:0.5:24:775 RRA:MIN:0.5:444:797  " %(rrdtool,filename,start,step,rrd_ds,rrd_dst)
    try:
        subprocess.call(cmd, shell=True)
    except:
        log.error('create rrd file %s failed' %(filename))


def update(filename,value):
    '''
    rrdtool update function
    '''
    cmd = "%s update %s \
    N:%s" %(rrdtool,filename,value)
    try:
        subprocess.call(cmd, shell=True)
    except:
        log.error('update rrd file %s failed' %(filename))


def graph(filename,rrd_file,rrd_ds,rrd_color):
    '''
    rrdtool graph function
    '''
    cmd = "%s graph %s \
                    DEF:v1=%s:%s:AVERAGE \
                    AREA:v1#%s" %(rrdtool,filename,rrd_file,rrd_ds,rrd_color)
    try:
        subprocess.call(cmd, shell=True)
    except:
        log.error('graph rrd file %s failed' %(filename))

def graph_combain(app_name,title):
    '''
    the app_name is also the yaml file's name,title is the rrdtool pic's title
    '''
    yaml_file = nginit.YAML_PATH +'/' + app_name + '.yaml'
    app = ngyaml(yaml_file)
    DEF = []


    print app

if __name__ == '__main__':
    graph_combain('base')


