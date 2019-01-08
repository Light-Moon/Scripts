import sys,os
import commands
import xmlUtils
from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger
from resource_management.libraries.script.script import Script

class Master(Script):
    def install(self, env):
        print 'Install My Master';
    def stop(self, env):
        status,output = commands.getstatusoutput("ls /")
        print 'status code: ', status
        print 'output: ', output
        Execute('rm -f /apps/dfs/dfs.pid')
        print "Stop My Master"
    def start(self, env):
        status,output = commands.getstatusoutput("ls ~")
        print 'status code: ', status
        print 'output: ', output
        print "Start My Master"
        config = Script.get_config()
		kv_dict = config['configurations']['dfs-site']
		commands.getstatus('rm ./../../configuration/zql1.xml')
		output_path = './../../configuration/zql.xml'
		write_xml(kv_dict, output_path)
       # Logger.info(config['configurations']['dfs-site']['dfs.supergroup'])
       # Logger.info(config['configurations']['dfs-site'])
        print 'configuration of dfs.supergroup:', config['configurations']['dfs-site']['dfs.supergroup']
        print 'configurations of dfs-site:', config['configurations']['dfs-site']
        print 'configurations of hbase-site:', config['configurations']['hbase-site']
       # tmp = Script.generate_configs_get_xml_file_content(self,'dfs-site','dfs2-site')
       # print 'tmp: ', tmp
       # File(['/apps/dfs/zql.xml'],mode=0755,owner='dfs',group='dfs',content='zzzzz')
       # Directory(['/apps/dfs/zql/dir1'],mode=0755,owner='dfs',group='dfs',create_parents=True)
    def status(self, env):
        pid =  format ("/apps/dfs/dfs.pid")
        check_process_status(pid)
        print 'Status of the My Master';
    def configure(self, env):
        print 'Configure the Sample Srv Master';
if __name__ == "__main__":
    Master().execute()