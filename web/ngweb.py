#!/usr/bin/env  python

from bottle import route ,run,template,TEMPLATE_PATH,static_file
TEMPLATE_PATH = 'views'

@route('/')
@route('/hello')
def greet(name='Stranger'):
    return template('index', name=name)
@route('/static_files/css/<filename>')
def server_static(filename):
    return static_file(filename,root='./static_files/css/', mimetype='text/css')
@route('/static_files/pic/rrd/<filename>')
def server_static(filename):
    return static_file(filename,root='./static_files/pic/rrd')
@route('/static_files/js/<filename>')
def server_static(filename):
    return static_file(filename,root='./static_files/js')
run(server="paste",host='0.0.0.0', port=8080)
