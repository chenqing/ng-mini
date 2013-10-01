#!/usr/bin/env python
#coding:utf-8
def get_output(cmd):
    '''
    好像是有的python版本的subprocess不存在check_output,所以要自己判断和封装一下
    利用commands.getoutput
    '''
    try:
        from subprocess import check_output
        return check_output(cmd,shell=True)
    except ImportError:
        from commands import getoutput
        return getoutput(cmd)