#!/usr/bin/env python
import sys
import os
os.sys.path.append(os.path.join(os.path.abspath('../') ,'modules'))
from ngsubprocess import get_output

cmd_in = "snmpget -v 2c -c public localhost ifInOctets.3|awk '{print $NF}'"
cmd_out = "snmpget -v 2c -c public localhost ifOutOctets.3|awk '{print $NF}'"

if sys.argv[1] == 'in':
    get_output(cmd_in)
elif sys.argv[1] == 'out':
    get_output(cmd_out)