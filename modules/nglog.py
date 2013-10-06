#!/usr/bin/env python
#coding:utf-8
import logging
import logging.handlers
import nginit

def nglog():
    '''
    处理ng的日志相关的函数
    '''
    if nginit.LOGED:
        logger = logging.getLogger()
        logger.setLevel(getattr(logging,nginit.LOG_LEVEL))
        File = logging.handlers.RotatingFileHandler(nginit.LOG_PATH,maxBytes=1024*1024,backupCount=5)
        Format = logging.Formatter("%(asctime)s   %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        File.setFormatter(Format)
        logger.addHandler(File)
        return logger

log = nglog()


