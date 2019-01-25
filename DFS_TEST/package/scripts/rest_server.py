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
            else:
                print file_path + ' is exist!' 
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            dfs_file_path = conf_dir + '/' + filename
            if not os.path.isfile(dfs_file_path):
                ln_cmd = 'ln -s ' + file_path + ' ' + dfs_file_path
                status,output = commands.getstatusoutput(ln_cmd)
                print 'ln_cmd status code : ', status
                print 'ln_cmd output : ', output
            else:
                print dfs_file_path + ' is exist!'
    def stop(self, env):
        print "Stop Rest Server"
        status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^" + Slave.superuser + ":")
        user_root_path=user_infos.split(':')[5]
        #pid =  format (user_root_path + "/ctdfs/pid/rest.pid")
        #status,output = commands.getstatusoutput("kill " + pid)
        status,output = commands.getstatusoutput("sudo -u " + Slave.superuser + " ps -ef|grep com.ctg.ctdfs.rest.server.Server |grep -v grep | awk '{print $2}' | xargs kill ")
        print 'kill rest status code: ', status
        print 'output: ', output
        status,output = commands.getstatusoutput("rm  " + user_root_path + "/ctdfs/pid/rest.pid")
        print 'rm rest.pid status code: ', status
        print 'output: ', output
    def start(self, env):
        print "Start Rest Server"
        current_path = os.getcwd()
        config = Script.get_config()
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
        status,output = commands.getstatusoutput("sudo -u " + Slave.superuser + " nohup sh " + user_root_path + "/ctdfs/bin/startRest.sh > " + user_root_path + "/ctdfs/logs/startRest.log \&")
        print 'status code: ', status
        print 'output: ', output
    def status(self, env):
        print "Status Rest Server"
        status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^" + Slave.superuser + ":")
        user_root_path=user_infos.split(':')[5]
        pid1 =  format (user_root_path + "/ctdfs/pid/rest.pid")
        print 'pid1 = ', pid1
        status,pid2 = commands.getstatusoutput("sudo -u " + Slave.superuser + " ps -ef|grep com.ctg.ctdfs.rest.server.Server |grep -v grep | awk '{print $2}'")
        print 'pid2 = ', pid2
        check_process_status(pid1)     
        #if pid2:
        #    raise ComponentIsNotRunning()
        print 'Status of the DFS_REST';   
    def configure(self, env):
        print "Configure Rest Server"
if __name__ == "__main__":
    Slave().execute()
