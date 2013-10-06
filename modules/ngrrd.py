#!/usr/bin/env python
#coding:utf-8
#import pyrrd //考虑到通用性还是使用封装命令行的方法吧
import subprocess
import os
import time
import nginit
from nglog import log
from ngyaml import ngyaml
from ngsubprocess import get_output

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

def graph_combain(app_name,title,vertical):
    '''
    the app_name is also the yaml file's name,title is the rrdtool pic's title
    '''
    font = nginit.FONT_PATH + '/' + 'DejaVuSansMono-Roman.ttf'
    graph_header = '%s graph %s/ng-mini.png -w 800 -h 500 \
    -t %s -v %s \
    -n TITLE:12:%s  -n LEGEND:8:%s \
    --start -86400 --end now \
    --slope-mode \
    --upper-limit 1500 \
    --disable-rrdtool-tag \
    -Y -X 0  ' %(nginit.RRDTOOL_PATH,nginit.PIC_PATH,title,vertical,font,font)
    graph_header += '-x MINUTE:30:HOUR:1:HOUR:1:0:"%H"' + ' \\ '

    yaml_file = nginit.YAML_PATH +'/' + app_name + '.yaml'
    app = ngyaml(yaml_file)
    graph_body_top = ''
    graph_body_center = ''
    graph_body_center += 'COMMENT:"\\n"         COMMENT:"\\n"         COMMENT:"\\t\\t最新值\\t\\t 平均值\\t\\t  最大值\\t\\t最小值\\n"'+' \\'
    graph_body_bottom = ''
    DS = []
    DEF = []
    CDEF = []
    METHOD = []
    COLOR = []
    RRA = ['LAST','MAX','AVERAGE','MIN']
    i = 0
    for a in app:
        rrd_file = nginit.RRD_PATH + '/' + app_name + '_' +a['Info'] + '.rrd'
        rrd_ds = a['RrdDs']
        DS.append(rrd_ds)
        METHOD.append(a['RrdMethod'].upper())
        COLOR.append('#'+a['Color'])
        DEF.append('DEF:v'+str(i)+'='+rrd_file+':'+rrd_ds+':AVERAGE')
        rrd_range = str(a['Range']).split(',')[0]
        if rrd_range.startswith('-'):
            CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+','+str(rrd_range).replace('-','')+', -')
        else:
            CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+','+str(rrd_range)+',+  ')
        graph_body_top += str(DEF[i] +' '+CDEF[i] )
        graph_body_bottom += str(METHOD[i]+':t'+str(i)+COLOR[i]+':'+DS[i] +\
                               ' GPRINT:v'+str(i)+':LAST:"%12.2lf" '+\
                                ' GPRINT:v'+str(i)+':MAX:"%12.2lf" '+\
                               ' GPRINT:v'+str(i)+':AVERAGE:"%12.2lf" '+\
                               ' GPRINT:v'+str(i)+':MIN:"%12.2lf" '+' COMMENT:"\\n" ')
        i = i+1
        if i >len(app):
            break
    print  graph_header
    print  graph_body_top + ' \\'
    print  graph_body_center
    print  graph_body_bottom


if __name__ == '__main__':
    yaml_file = nginit.YAML_PATH +'/base.yaml'
    app = ngyaml(yaml_file)
    graph_combain('base','本机rrdtool','汇总图')


