#!/usr/bin/env python
#coding:utf-8
import yaml
import nginit
from  nglog import log

def ngyaml(filename):
    '''
    解析yaml配置文件
    '''
    d = {}
    try:
        f = open(filename)
        d = yaml.safe_load(f)
    except:
        log.error('can\'t open the yaml file %s' %(filename))
    return d
