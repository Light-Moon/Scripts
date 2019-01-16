import sys,os
import commands
from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger

class Slave(Script):
    def install(self, env):
        print 'Install the Rest Server';
    def stop(self, env):
        print "Stop Rest Server"
        status,output = commands.getstatusoutput("ls /apps/dfs")
        print 'status code: ', status
        print 'output: ', output
        Execute('rm -f /apps/dfs/dfs_slave.pid')
    def start(self, env):
        print "Start Rest Server"
        status,output = commands.getstatusoutput("ls")
        print 'status code: ', status
        print 'output: ', output
    def status(self, env):
        print "Status Rest Server"
        pid =  format ("/apps/dfs/dfs_slave.pid")
        check_process_status(pid)
    def configure(self, env):
        print "Configure Rest Server"
if __name__ == "__main__":
    Slave().execute()
