#!/usr/bin/env python
#coding:utf-8
import sys
import os
import subprocess
import time
os.sys.path.append(os.path.join(os.path.abspath('.') ,'modules'))
import nginit
from nglog import log
import ngrrd
from ngdaemon import *
from ngyaml import ngyaml
from ngsubprocess import get_output

class Ngd(Daemon):
    def __init__(self, pidfile):
        Daemon.__init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')
        self._pre_check()
        self.time_start = int(time.time())

    def _pre_check(self):
        '''
        检查是不是还有需要创建rrd的没有创建
        '''
        for apps in nginit.APPS:
            app_yaml = nginit.YAML_PATH + '/' + apps + '.yaml'
            yaml_list = ngyaml(app_yaml)
            for yaml in yaml_list:
                rrd_file = nginit.RRD_PATH + '/' + apps + '_' + yaml['Info'] + '.rrd'
                if not os.path.isfile(rrd_file) and yaml['CreatePic']:
                    ngrrd.create(rrd_file,yaml['RrdDs'],yaml['RrdDst'],yaml['TimeInterval'])

    def run(self):
        while True:
            time.sleep(60)
            for apps in nginit.APPS:
                app_yaml = nginit.YAML_PATH + '/' + apps + '.yaml'
                yaml_list = ngyaml(app_yaml)
                for yaml in yaml_list:
                    rrd_file = nginit.RRD_PATH + '/' + apps + '_' + yaml['Info'] + '.rrd'
                    interval = yaml['TimeInterval']
                    print interval
                    if interval > 5:
                        interval = 5
                    if (int(time.time()) - self.time_start) % (interval * 60 ) == 0:
                        value = get_output(yaml['CmdLine'])

                        ngrrd.update(rrd_file,value)



if __name__ == "__main__":
    daemon = Ngd(nginit.PID)
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
