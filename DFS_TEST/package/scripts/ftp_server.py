import sys,os
import commands
from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger

class Slave(Script):
    def install(self, env):
        print 'Install the Ftp Server';
    def stop(self, env):
        print "Stop Ftp Server"
        status,output = commands.getstatusoutput("ls /apps/dfs")
        print 'status code: ', status
        print 'output: ', output
        Execute('rm -f /apps/dfs/dfs_slave.pid')
    def start(self, env):
        print "Start Ftp Server"
        status,output = commands.getstatusoutput("ls")
        print 'status code: ', status
        print 'output: ', output
    def status(self, env):
        print "Status Ftp Server"
        pid =  format ("/apps/dfs/dfs_slave.pid")
        check_process_status(pid)
    def configure(self, env):
        print "Configure Ftp Server"
if __name__ == "__main__":
    Slave().execute()
