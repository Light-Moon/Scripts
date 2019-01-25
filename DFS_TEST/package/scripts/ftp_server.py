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
        print 'Install the FTP Server';        
        config = Script.get_config()
        Slave.superuser = config['configurations']['dfs-site']['dfs.superuser']
        print 'Current superuser is : ', Slave.superuser
        current_path = os.getcwd()
        dfs_conf_dir = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/configuration'		
        filenames = ['ctdfs-ambari-site.xml']
        status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^" + Slave.superuser + ":")
        print 'status code : ', status
        print 'user_infos output : ', user_infos
        user_root_path=user_infos.split(':')[5]
        print 'user_root_path is : ', user_root_path
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
                print 'ln_cmd status code : ', status
                print 'ln_cmd output : ', output
    def stop(self, env):
        print "Stop Ftp Server"
        status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^" + Slave.superuser + ":")
        user_root_path=user_infos.split(':')[5]
        #pid =  format (user_root_path + "/ctdfs/pid/ftp.pid")
        #status,output = commands.getstatusoutput("kill " + pid)
        status,output = commands.getstatusoutput("sudo -u " + Slave.superuser + " ps -ef|grep ctdfs-ftp |grep -v grep | awk '{print $2}' | xargs kill ")
        print 'kill ftp status code: ', status
        print 'output: ', output
        status,output = commands.getstatusoutput("rm  " + user_root_path + "/ctdfs/pid/ftp.pid")
        print 'rm ftp.pid status code: ', status
        print 'output: ', output
    def start(self, env):
        print "Start FTP Server"
        current_path = os.getcwd()
        config = Script.get_config()
        dfs_conf_dir = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/configuration'		
        filenames = ['ctdfs-ambari-site.xml']
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
        status,output = commands.getstatusoutput("sudo -u " + Slave.superuser + " nohup sh " + user_root_path + "/ctdfs/bin/startFtp.sh > " + user_root_path + "/ctdfs/logs/startFtp.log \&")
        print 'status code: ', status
        print 'output: ', output
    def status(self, env):
        print "Status Ftp Server"
        status,user_infos=commands.getstatusoutput("cat /etc/passwd|grep ^" + Slave.superuser + ":")
        user_root_path=user_infos.split(':')[5]
        pid = format(user_root_path + "/ctdfs/pid/ftp.pid")
        status,pid2 = commands.getstatusoutput("sudo -u " + Slave.superuser + " ps -ef|grep NameNode |grep -v grep | awk '{print $2}'")
        check_process_status(pid)
        print 'pid2 = ', pid2
        #if pid:
        #    raise ComponentIsNotRunning()
        print 'Status of the DFS_FTP';
    def configure(self, env):
        print "Configure Ftp Server"
if __name__ == "__main__":
    Slave().execute()
