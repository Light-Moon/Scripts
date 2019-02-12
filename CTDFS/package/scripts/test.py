#coding=utf-8
import sys,os
import commands
import xml_utils
from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger
from resource_management.libraries.script.script import Script
from xml_utils import write_xml
def start():
    status,pid = commands.getstatusoutput("ps -ef|grep NameNode  |                                                                                   grep -v grep | awk '{print $2}'")
    status,pid2 = commands.getstatusoutput("ps -ef|grep NameNode  |  grep -v grep | awk '{print $2}'")
    print 'pid2=', pid2
    #check_process_status(pid)
    #if pid:
    #    raise ComponentIsNotRunning()
    #    print 'ComponentIsNotRunning'
    print 'Status of the DFS_MASTER', pid  
