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

class Slave(Script):
    #config = Script.get_config()
    #superuser = config['configurations']['dfs-site']['dfs.superuser']
    superuser = 'autodfs'
    print 'Default superuser is : ', superuser    
    def install(self, env):
        print 'Install the Rest Server';
        config = Script.get_config()
        Slave.superuser = config['configurations']['dfs-site']['dfs.superuser']
        print 'Current superuser is : ', Slave.superuser
        current_path = os.getcwd()
        dfs_conf_dir = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/configuration'		
        filenames = ['ctdfs-rest-site.xml']
        status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^" + Slave.superuser + ":")
        user_root_path=user_infos.split(':')[5]        
        conf_dir = user_root_path + '/ctdfs/conf'
        for filename in filenames:
            print 'origin filename=', filename
            # filename = filename.split('/')[-1]
            file_path = dfs_conf_dir + '/' + filename
            print 'file_path=', file_path
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner='autodfs',group='autodfs')
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            dfs_file_path = conf_dir + '/' + filename
            if not os.path.isfile(dfs_file_path):
                ln_cmd = 'ln -s ' + file_path + ' ' + dfs_file_path
                status,output = commands.getstatusoutput(ln_cmd)
    def stop(self, env):
        print "Stop Rest Server"
        status,output = commands.getstatusoutput("ls /apps/dfs")
        print 'status code: ', status
        print 'output: ', output
        Execute('rm -f /apps/dfs/dfs_slave.pid')
    def start(self, env):
        print "Start Rest Server"
        dfs_conf_dir = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/configuration'		
        filenames = ['ctdfs-rest-site.xml']
        status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^" + Slave.superuser + ":")
        user_root_path=user_infos.split(':')[5]
        conf_dir = user_root_path + '/ctdfs/conf'
        for filename in filenames:
            print 'origin filename=', filename
            # filename = filename.split('/')[-1]
            file_path = dfs_conf_dir + '/' + filename
            print 'file_path=', file_path
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner='autodfs',group='autodfs')
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            dfs_file_path = conf_dir + '/' + filename
            if not os.path.isfile(dfs_file_path):
                ln_cmd = 'ln -s ' + file_path + ' ' + dfs_file_path
                status,output = commands.getstatusoutput(ln_cmd)
        status,output = commands.getstatusoutput("sudo -u " + Slave.superuser + " nohup " + user_root_path + "/ctdfs/bin/startRest.sh > " + user_root_path + "/ctdfs/log/startRest.log &")
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
