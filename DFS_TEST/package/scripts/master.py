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

class Master(Script):
    config = Script.get_config()
   # print 'configurations of dfs-site:', config['configurations']['dfs-site']
   # superuser = config['configurations']['dfs-site']['dfs.superuser']
   # supergroup = config['configurations']['dfs-site']['dfs.supergroup']
   # install_package_path = config['configurations']['dfs-site']['dfs.installpack.path']
    superuser = 'autodfs'
    supergroup = 'dfs'
    install_package_path = '/apps/ctdfs.tar.gz'
    print "Default superuser is [" + superuser + "]"
    print "Default supergroup is [" + supergroup + "]"
    print "Default install_package_path is [" + install_package_path + "]"
    def install(self, env):
        print 'Install DFS_MASTER';
        config = Script.get_config()
        Master.superuser = config['configurations']['dfs-site']['dfs.superuser']
        Master.supergroup = config['configurations']['dfs-site']['dfs.supergroup']
        Master.install_package_path = config['configurations']['dfs-site']['dfs.installpack.path']
        print "Current superuser is [" + Master.superuser + "]"
        print "Current supergroup is [" + Master.supergroup + "]"
        print "Current install_package_path is [" + Master.install_package_path + "]"
        current_path = os.getcwd()
        scripts_path = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/package/scripts'
        status,output = commands.getstatusoutput("sh " + scripts_path + "/test.sh -u " + Master.superuser + " -g " + Master.supergroup + " -p " + Master.install_package_path + " >> " + scripts_path + "/dfs-deploy.log")
        print 'install status code: ', status
        print 'install output: ', output
    def stop(self, env):
        print "Stop DFS_MASTER"
    def start(self, env):
        print "Start DFS_MASTER"
        status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^" + Master.superuser + ":")
        #substr=commands.getoutput("${user_infos##*::}")
        #user_root_path=commands.getoutput("${substr%%:*}")
        #conf_dir = '${user_root_path}/ctdfs/conf'
        substr=commands.getoutput("${" + user_infos + "##*::}")
        user_root_path=commands.getoutput("${" + substr + "%%:*}")
        conf_dir = user_root_path + '/ctdfs/conf'
        config = Script.get_config()
        current_path = os.getcwd()
        dfs_conf_dir = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/configuration'
        if not os.path.isdir(dfs_conf_dir):
           # os.mkdir(dfs_conf_dir)   2选1即可
            Directory([dfs_conf_dir],mode=0755,owner=Master.superuser,group=Master.supergroup,create_parents=True) 
        #filenames = ['dfs-site.xml']
        status,filenames = commands.getstatusoutput("find " + dfs_conf_dir + " -name *.xml -o -name *.properties -type f -maxdepth 1")
        print 'find xxx status code: ', status
        print 'find xxx output: ', filenames
        print 'filenames is', filenames
        for filename in filenames:
            print 'origin filename=', filename
            filename = filename.split('/')[-1]
            file_path = dfs_conf_dir + '/' + filename
            print 'file_path=', file_path
            if not os.path.isfile(file_path):
               # f = open(file_path, 'w')
               # f.close() 上面两句等同于下一句，2选1即可
                File([file_path],mode=0755,owner='autodfs',group='autodfs')
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = config['configurations'][prefix_filename]
            #dict = config['configurations']['dfs-site']
            write_xml(dict, file_path)
            dfs_file_path = conf_dir + '/' + filename
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
    def status(self, env):
        pid =  format ("/apps/dfs/dfs.pid")
        check_process_status(pid)
        print 'Status of the DFS_MASTER';
    def configure(self, env):
        print 'Configure the Sample Srv Master';
if __name__ == "__main__":
    Master().execute()
   # Master().execute().start(self,env)
