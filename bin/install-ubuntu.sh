#!/bin/bash
# this script is help you install the ng-mini client in ubuntu
# author qing.chen

sudo apt-get install python-yaml rrdtool

sudo wget -O /tmp/ng-mini.0.1.beta.tgz http://www.chenqing.org/soft/ng-mini.0.1.beta.tgz

sudo tar zvxf /tmp/ng-mini.0.1.beta.tgz -C /usr/local/
sudo cp /usr/local/ng-mini/bin/ng-client /etc/init.d/
