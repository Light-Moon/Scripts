import sys,os
import commands
import xml_utils
from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger
from resource_management.libraries.script.script import Script
from xml_utils import write_xml

class Master(Script):
    dfs_conf_dir = '/apps/dfs'
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
        config = Script.get_config()
        current_path = os.getcwd()
        conf_dir = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/configuration'
        if not os.path.isdir(conf_dir):
           # os.mkdir(conf_dir)   
            Directory([conf_dir],mode=0755,owner='dfs',group='dfs',create_parents=True) 
        filenames = ['dfs-site.xml']
        for filename in filenames:
            file_path = conf_dir + '/' + filename
            if not os.path.isfile(file_path):
               # f = open(file_path, 'w')
               # f.close()
                File([file_path],mode=0755,owner='dfs',group='dfs')
            prefix_filename = filename[:-4]
            dict = config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            dfs_file_path = Master.dfs_conf_dir + '/' + filename
            if not os.path.isfile(dfs_file_path):
                ln_cmd = 'ln -s ' + file_path + ' ' + dfs_file_path
                status,output = commands.getstatusoutput(ln_cmd)
                print "execute 'ln' status code: ", status
       # status,output = commands.getstatusoutput("pwd")
       # print 'status code: ', status
       # print 'output: ', output
       # commands.getstatus('rm ./../../configuration/zql1.xml')
       # output_path = './../../configuration/zql.xml'
       # output_path = output + '/zql.xml'
       # File([output_path],mode=0755,owner='dfs',group='dfs',content='zzzzz')
       # write_xml(dict, output_path)
       # Logger.info(config['configurations']['dfs-site']['dfs.supergroup'])
       # Logger.info(config['configurations']['dfs-site'])
        print 'configuration of dfs.supergroup:', config['configurations']['dfs-site']['dfs.supergroup']
        print 'configurations of dfs-site:', config['configurations']['dfs-site']
        print 'configurations of hbase-site:', config['configurations']['hbase-site']
       # tmp = Script.generate_configs_get_xml_file_content(self,'dfs-site','dfs2-site')
       # print 'tmp: ', tmp
       # File(['/apps/dfs/zql.xml'],mode=0755,owner='dfs',group='dfs',content='zzzzz')
       # Directory(['/apps/dfs/zql/dir1'],mode=0755,owner='dfs',group='dfs',create_parents=True)
        print "Start My Master"
    def status(self, env):
        pid =  format ("/apps/dfs/dfs.pid")
        check_process_status(pid)
        print 'Status of the My Master';
    def configure(self, env):
        print 'Configure the Sample Srv Master';
if __name__ == "__main__":
    Master().execute()
   # Master().execute().start(self,env)
