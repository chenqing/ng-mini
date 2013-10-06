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
from signal import SIGKILL
child_pid = -1
class Ngd(Daemon):
    def __init__(self, pidfile):
        Daemon.__init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')
        self._pre_check()
        self.time_start = int(time.time())
#	self.run()

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
    def _start_web_server(self):
        '''
	'''
	#start web server
	os.chdir(nginit.APP_PATH + '/' + 'web')
	child = subprocess.Popen(['python', 'ngweb.py'])
	if not child.pid:
		log.error('start web server fail')
		sys.exit()
	child_pid = child.pid

    def run(self):
	'''
	'''
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
                    if interval > 5:
                        interval = 5
                    #if (int(time.time()) - self.time_start) % (interval * 60 ) == 0:
                    if 60 % interval == 0:
			value = 0
                        if yaml['UseApp']:
                            cmd = nginit.APPS_PATH + '/' +yaml['CmdLine']
                            value = get_output(cmd)
			    #print cmd,value
                        else:
                            value = get_output(yaml['CmdLine'])
			try:
                        	ngrrd.update(rrd_file,str(value).rstrip(','))
				log.info('update '+rrd_file+' value is ' +str(value).rstrip(','))
			except:
				log.error('update '+rrd_file+' value is ' +str(value).rstrip(',')+' error')


if __name__ == "__main__":
    daemon = Ngd(nginit.PID)
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            pid = get_output("ps -ef |grep ngweb|grep -v grep |awk '{print $2}'")
	    subprocess.call(['kill',pid])
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
