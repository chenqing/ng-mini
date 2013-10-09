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

def graph_combain(app_name,title,vertical,date='day'):
    '''
    the app_name is also the yaml file's name,title is the rrdtool pic's title
    '''
    dt = {'day':86400,'week':604800,'month':2592000,'year':31536000}
    if date not in ['day','week','month','year']:
        date = 'day'
    font = nginit.FONT_PATH + '/' + 'msyh.ttf'
    graph_header = '%s graph %s/ng-mini-%s.png -w 600 -h 300 \
    -t "%s" -v "%s" \
    -n TITLE:12:%s  -n LEGEND:8:%s \
    --start -%s --end now \
    --slope-mode \
    --upper-limit 1500 \
    -Y  --base=1000   --upper-limit 1500      -l 0 ' %(nginit.RRDTOOL_PATH,nginit.PIC_PATH,date,title,vertical,font,font,dt[date])
    if date == 'day':
        graph_header += '-x MINUTE:30:HOUR:1:HOUR:1:0:"%H" '

    yaml_file = nginit.YAML_PATH +'/' + app_name + '.yaml'
    app = ngyaml(yaml_file)
    graph_body_top = ''
    graph_body_center = ''
    graph_body_bottom = ''
    DS = []
    DEF = []
    CDEF = []
    METHOD = []
    COLOR = []
    RRA = ['LAST','MAX','AVERAGE','MIN']
    i = 0
    for a in app:
        if a['CreatePic']:
            rrd_file = nginit.RRD_PATH + '/' + app_name + '_' +a['Info'] + '.rrd'
            rrd_ds = a['RrdDs']
            DS.append(rrd_ds)
            METHOD.append(a['RrdMethod'].upper())
            COLOR.append('#'+a['Color'])
            DEF.append('DEF:v'+str(i)+'='+rrd_file+':'+rrd_ds+':AVERAGE')
            rrd_range = str(a['Range']).split(',')[0]
            if rrd_range.startswith('-'):
                if a['Info'].startswith('BAND_WIDTH'):
                    CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+',8,*, ' + str(rrd_range).replace('-','')+', - ')
		else:
                    CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+','+str(rrd_range).replace('-','')+', - ')
            else:
                if a['Info'].startswith('BAND_WIDTH'):
                    CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+',8,*,' + str(rrd_range)+',+ ')
		else:
                    CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+','+str(rrd_range)+',+  ')
            graph_body_top += str(DEF[i] +' '+CDEF[i] )
            if a['Info'].startswith('BAND_WIDTH'):
            	graph_body_bottom += str(METHOD[i]+':t'+str(i)+COLOR[i]+':'+ '\" ' + DS[i] + '\"' +\
                                   ' GPRINT:t'+str(i)+':LAST:"LAST %6.2lf %Sbps" '+\
                                    ' GPRINT:t'+str(i)+':MAX:"MAX %6.2lf %Sbps" '+\
                                   ' GPRINT:t'+str(i)+':AVERAGE:"AVERAGE %6.2lf %Sbps" '+\
                                   ' GPRINT:t'+str(i)+':MIN:"MIN %6.2lf %Sbps" '+' COMMENT:"\\n" ')
            else:
            	graph_body_bottom += str(METHOD[i]+':t'+str(i)+COLOR[i]+':'+ '\" ' + DS[i] + '\"' +\
                                   ' GPRINT:v'+str(i)+':LAST:"LAST %6.2lf " '+\
                                    ' GPRINT:v'+str(i)+':MAX:"MAX %6.2lf " '+\
                                   ' GPRINT:v'+str(i)+':AVERAGE:"AVERAGE %6.2lf " '+\
                                   ' GPRINT:v'+str(i)+':MIN:"MIN %6.2lf " '+' COMMENT:"\\n" ')
            	
            i = i+1
            if i >len(app):
                break
    graph_total = graph_header + graph_body_top + ' ' + graph_body_center + ' ' + graph_body_bottom
    subprocess.call(str(graph_total),shell=True)

def graph_combain_without_network(app_name,title,vertical,date='day'):
    '''
    the app_name is also the yaml file's name,title is the rrdtool pic's title
    '''
    dt = {'day':86400,'week':604800,'month':2592000,'year':31536000}
    if date not in ['day','week','month','year']:
        date = 'day'
    font = nginit.FONT_PATH + '/' + 'msyh.ttf'
    graph_header = '%s graph %s/ng-mini-%s.png -w 600 -h 300 \
    -t "%s" -v "%s" \
    -n TITLE:12:%s  -n LEGEND:8:%s \
    --start -%s --end now \
    --slope-mode \
    -Y -X 0        -l 0 ' %(nginit.RRDTOOL_PATH,nginit.PIC_PATH,date,title,vertical,font,font,dt[date])
    if date == 'day':
        graph_header += '-x MINUTE:30:HOUR:1:HOUR:1:0:"%H" '

    yaml_file = nginit.YAML_PATH +'/' + app_name + '.yaml'
    app = ngyaml(yaml_file)
    graph_body_top = ''
    graph_body_center = ''
    graph_body_bottom = ''
    DS = []
    DEF = []
    CDEF = []
    METHOD = []
    COLOR = []
    RRA = ['LAST','MAX','AVERAGE','MIN']
    i = 0
    for a in app:
        if a['CreatePic'] and not a['Info'].startswith('BAND_WIDTH'):
            rrd_file = nginit.RRD_PATH + '/' + app_name + '_' +a['Info'] + '.rrd'
            rrd_ds = a['RrdDs']
            DS.append(rrd_ds)
            METHOD.append(a['RrdMethod'].upper())
            COLOR.append('#' + str(a['Color']))
            DEF.append('DEF:v'+str(i)+'='+rrd_file+':'+rrd_ds+':AVERAGE')
            rrd_range = str(a['Range']).split(',')[0]
            if rrd_range.startswith('-'):
                CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+','+str(rrd_range).replace('-','')+', - ')
            else:
                CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+','+str(rrd_range)+',+  ')
            graph_body_top += str(DEF[i] +' '+CDEF[i] )
            graph_body_bottom += str(METHOD[i]+':t'+str(i)+COLOR[i]+':'+ '\" ' + DS[i] + '\"' +\
                                   ' GPRINT:v'+str(i)+':LAST:"LAST %6.2lf " '+\
                                    ' GPRINT:v'+str(i)+':MAX:"MAX %6.2lf " '+\
                                   ' GPRINT:v'+str(i)+':AVERAGE:"AVERAGE %6.2lf " '+\
                                   ' GPRINT:v'+str(i)+':MIN:"MIN %6.2lf " '+' COMMENT:"\\n" ')

            i = i+1
            if i >len(app):
                break
    graph_total = graph_header + graph_body_top + ' ' + graph_body_center + ' ' + graph_body_bottom
    subprocess.call(str(graph_total),shell=True)

def graph_network(app_name,title,vertical,date='day'):
    '''
    the app_name is also the yaml file's name,title is the rrdtool pic's title
    '''
    dt = {'day':86400,'week':604800,'month':2592000,'year':31536000}
    if date not in ['day','week','month','year']:
        date = 'day'
    font = nginit.FONT_PATH + '/' + 'msyh.ttf'
    graph_header = '%s graph %s/ng-mini-network-%s.png -w 600 -h 300 \
    -t "%s" -v "%s" \
    -n TITLE:12:%s  -n LEGEND:8:%s \
    --start -%s --end now \
    --slope-mode \
    --upper-limit 1500 \
    -Y  --base=1000   --upper-limit 1500      -l 0 ' %(nginit.RRDTOOL_PATH,nginit.PIC_PATH,date,title,vertical,font,font,dt[date])
    if date == 'day':
        graph_header += '-x MINUTE:30:HOUR:1:HOUR:1:0:"%H" '

    yaml_file = nginit.YAML_PATH +'/' + app_name + '.yaml'
    app = ngyaml(yaml_file)
    graph_body_top = ''
    graph_body_center = ''
    graph_body_bottom = ''
    DS = []
    DEF = []
    CDEF = []
    METHOD = []
    COLOR = []
    RRA = ['LAST','MAX','AVERAGE','MIN']
    i = 0
    for a in app:
        if a['CreatePic'] and a['Info'].startswith('BAND_WIDTH'):
            rrd_file = nginit.RRD_PATH + '/' + app_name + '_' +a['Info'] + '.rrd'
            rrd_ds = a['RrdDs']
            DS.append(rrd_ds)
            METHOD.append(a['RrdMethod'].upper())
            COLOR.append('#'+a['Color'])
            DEF.append('DEF:v'+str(i)+'='+rrd_file+':'+rrd_ds+':AVERAGE')
            rrd_range = str(a['Range']).split(',')[0]
            if rrd_range.startswith('-'):
                CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+',8,*, ' + str(rrd_range).replace('-','')+', - ')
            else:
                CDEF.append('CDEF:t'+str(i)+'=v'+str(i)+',8,*,' + str(rrd_range)+',+ ')
            graph_body_top += str(DEF[i] +' '+CDEF[i] )
            graph_body_bottom += str(METHOD[i]+':t'+str(i)+COLOR[i]+':'+ '\" ' + DS[i] + '\"' +\
                                   ' GPRINT:t'+str(i)+':LAST:"LAST %6.2lf %Sbps" '+\
                                    ' GPRINT:t'+str(i)+':MAX:"MAX %6.2lf %Sbps" '+\
                                   ' GPRINT:t'+str(i)+':AVERAGE:"AVERAGE %6.2lf %Sbps" '+\
                                   ' GPRINT:t'+str(i)+':MIN:"MIN %6.2lf %Sbps" '+' COMMENT:"\\n" ')
            	
            i = i+1
            if i >len(app):
                break
    graph_total = graph_header + graph_body_top + ' ' + graph_body_center + ' ' + graph_body_bottom
    subprocess.call(str(graph_total),shell=True)

if __name__ == '__main__':
    yaml_file = nginit.YAML_PATH +'/base.yaml'
    app = ngyaml(yaml_file)
    graph_combain('base',time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime()),'汇总图','day')



if __name__ == '__main__':
    yaml_file = nginit.YAML_PATH +'/base.yaml'
    app = ngyaml(yaml_file)
    graph_combain('base',time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime()),'汇总图','day')


