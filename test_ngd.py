#!/usr/bin/env python
#coding:utf-8
import sys
import os
import subprocess
import time
from datetime import datetime
from signal import SIGTERM
#from modules directory import ng-mini modules
from modules import nginit                  # init some global variable used in this file
from modules.nglog import log               # Encapsulated logging standard library for log record
from modules import ngrrd                   # Encapsulated rrdtool module
from modules.ngdaemon import Daemon         # demonize module
from modules.ngyaml import ngyaml           # yaml module
from modules.ngsubprocess import get_output # Encapsulated subprocess and commands module to get cmd output

class Ngd(Daemon):
    """
    demonize ,used for  collect data read from app's yaml ,create rra file(rrdtool database),update data in rra
	start or stop web server which used bottle web micro framework
    """

    def __init__(self,pidfile):
        """
        Inherit from the ngdaemon which is a class used to create daemonize program in python
        """
        Daemon.__init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')
        self._pre_check()
#        self.run()

    def _pre_check(self):
        """
        when start this script,may be check the rrd file is already create (it's may be new task add in yaml file )
        """
        for apps in nginit.APPS:
            app_yaml = nginit.YAML_PATH + '/' + apps + '.yaml'
            yaml_list = ngyaml(app_yaml)
            for yaml in yaml_list:
                rrd_file = nginit.RRD_PATH + '/' + apps + '_' + yaml['Info'] + '.rrd'
                if not os.path.isfile(rrd_file) and yaml['CreatePic']:
                    ngrrd.create(rrd_file,yaml['RrdDs'],yaml['RrdDst'],yaml['TimeInterval'])

    def _start_web_server(self):
        """
        a micro web server use bottle
        """
        os.chdir(nginit.APP_PATH + '/' + 'web')
        child = subprocess.Popen([nginit.PY_PATH,'ngweb.py'])
        if not child.pid:
            log.error('web server start failed')
            sys.exit(2)

    def stop(self):
        """
        Inherit from Daemon and add stop ngweb.py
        """
        Daemon.stop(self)
        web_pid = get_output("ps -ef |grep ngweb|grep -v grep |awk '{print $2}'")
        try:
            os.kill(int(web_pid),SIGTERM)
        except:
            log.error('stop web server failed')

    def run(self):
        """
        this will be run in background ,collect data
        """
        #start web server
        try:
            self._start_web_server()
        except:
            pass

        while True:
            time.sleep(60)
            for apps in nginit.APPS:
                app_yaml = nginit.YAML_PATH + '/' + apps + '.yaml'
                yaml_list = ngyaml(app_yaml)
                for yaml in yaml_list:
                    rrd_file = nginit.RRD_PATH + '/' + apps + '_' + yaml['Info'] + '.rrd'
                    interval = yaml['TimeInterval']
                    value = 0
                    if interval > 5:
                        interval = 5
                    if datetime.now().minute % interval == 0:
                        if yaml['UseApp']:
                            cmd = nginit.APPS_PATH + '/' +yaml['CmdLine']
                            value = get_output(cmd)
                        else:
                            value = get_output(yaml['CmdLine'])
                    ngrrd.update(rrd_file,str(value).rstrip(','))
                    log.info('update ' + rrd_file + ' value is ' + str(value).rstrip(','))
                    if datetime.now().minute % 2 == 0:
                        hostname = get_output('hostname')
                        for dt in ['day','week','month','year']:
                            title =  hostname + ' Last update:'  + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + ' ' + dt +' Graph' 
			    print title
			    ngrrd.graph_combain('base',title,'cpis bit/s',dt)
			    log.info('base app graph ok')

if __name__ == '__main__':
    ng = Ngd(nginit.PID)
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            ng.start()
        elif 'stop' == sys.argv[1]:
            ng.stop()
        elif 'restart' == sys.argv[1]:
            ng.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

