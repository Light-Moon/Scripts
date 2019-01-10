import sys,os
import commands
from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger

class Slave(Script):
    def install(self, env):
        print 'Install the Sample Srv Slave';
    def stop(self, env):
        status,output = commands.getstatusoutput("ls /apps/dfs")
        print 'status code: ', status
        print 'output: ', output
        Execute('rm -f /apps/dfs/dfs_slave.pid')
        print "Stop My Slave" 
    def start(self, env):
        status,output = commands.getstatusoutput("ls")
        print 'status code: ', status
        print 'output: ', output
        print "Start My Slave" 
    def status(self, env):
        pid =  format ("/apps/dfs/dfs_slave.pid")
        check_process_status(pid)
        print 'Status of the My Slave';  
    def configure(self, env):
        print 'Configure the Sample Srv Slave';
if __name__ == "__main__":
    Slave().execute()
