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
    def install(self, env):
        print 'Install DFS_MASTER';
        current_path = os.getcwd()
        scripts_path = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/package/scripts'
        status,output = commands.getstatusoutput("sh " + scripts_path + "/dfs-deploy.sh >> " + scripts_path + "/dfs-deploy.log")
        print 'install status code: ', status
        print 'install output: ', output
    def stop(self, env):
        print "Stop DFS_MASTER"
    def start(self, env):
        # status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^dfs:")
        status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^autodfs:")
        substr=commands.getoutput("${user_infos##*::}")
        user_root_path=commands.getoutput("${substr%%:*}")
        dfs_conf_dir = '${user_root_path}/ctdfs/conf'
        config = Script.get_config()
        current_path = os.getcwd()
        conf_dir = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/configuration'
        if not os.path.isdir(conf_dir):
           # os.mkdir(conf_dir)   
           # Directory([conf_dir],mode=0755,owner='dfs',group='dfs',create_parents=True) 
            Directory([conf_dir],mode=0755,owner='autodfs',group='autodfs',create_parents=True) 
        # filenames = ['dfs-site.xml']
        filenames = commands.getoutput("find " + conf_dir + " '*.xml' -o '*.properties' -type f -maxdepth 1")
        for filename in filenames:
            filename = filename.split('/')[-1]
            file_path = conf_dir + '/' + filename
            if not os.path.isfile(file_path):
               # f = open(file_path, 'w')
               # f.close()
                File([file_path],mode=0755,owner='autodfs',group='autodfs')
            prefix_filename = filename[:-4]
            dict = config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            dfs_file_path = dfs_conf_dir + '/' + filename
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
        print "Start DFS_MASTER"
    def status(self, env):
        pid =  format ("/apps/dfs/dfs.pid")
        check_process_status(pid)
        print 'Status of the DFS_MASTER';
    def configure(self, env):
        print 'Configure the Sample Srv Master';
if __name__ == "__main__":
    Master().execute()
   # Master().execute().start(self,env)
