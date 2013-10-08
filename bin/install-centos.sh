#!/bin/bash
# this script is help you install the ng-mini client
# authon qing.chen

os_version=`awk '{printf "%d" ,$3}' /etc/redhat-release`
if [ $os_version -lt 5 ];then
	echo 'need centos 5 or newer'
	exit 254
fi
if [ $os_version -eq 5 ];then
    if ! rpm -ql epel-release ;then
	if rpm -Uvh http://mirrors.sohu.com/fedora-epel/5/x86_64/epel-release-5-4.noarch.rpm ;then
		yum -y install rrdtool PyYAML python26
	fi
     else
		yum -y install rrdtool PyYAML python26
    fi
fi

if [ $os_version -eq 6 ];then
    if ! rpm -ql epel-release ;then
        if  rpm -Uvh http://mirrors.sohu.com/fedora-epel/6/x86_64/epel-release-6-8.noarch.rpm ;then
               yum -y install rrdtool PyYAML     
        fi
    else
		yum -y install rrdtool PyYAML
    fi
fi

wget -O /tmp/ng-mini.0.1.beta.tgz http://www.chenqing.org/soft/ng-mini.0.1.beta.tgz

tar zvxf /tmp/ng-mini.0.1.beta.tgz -C /usr/local/
cp /usr/local/ng-mini/bin/ng-client /etc/init.d/
