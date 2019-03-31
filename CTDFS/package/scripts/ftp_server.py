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

class Ftp(Script):
    FTP_PID_DIR=''
    superuser=''
    def install(self, env):
        import params
        env.set_params(params)
        print "********** Install CTDFS_FTP Operation Begin **********" 
        if not os.path.isdir(params.ctdfs_conf_dir):
            Directory([params.ctdfs_conf_dir],mode=0755,owner=params.superuser,group=params.supergroup,create_parents=True)    
        for filename in params.ctdfs_ftp_conf_filenames:
            print 'ctdfs_ftp_conf_filename = ', filename
            file_path = params.ctdfs_conf_dir + '/' + filename
            print 'file_path = ', file_path
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            ftp_target_file_path = params.target_conf_dir + '/' + filename
            if not os.path.isfile(ftp_target_file_path):
                ln_cmd = 'ln -s ' + file_path + ' ' + ftp_target_file_path
                status,output = commands.getstatusoutput(ln_cmd)
                print 'Execute ln_cmd status code : ', status
                print 'Execute ln_cmd output : ', output
        print "********** Install CTDFS_FTP Operation End **********" 
    def stop(self, env):
        import params
        env.set_params(params)
        print "********** Stop CTDFS_FTP Operation Begin **********"         
        #这里应该用读pid文件中的进程号进行kill
        status,output = commands.getstatusoutput("sudo -u " + params.superuser + " ps -ef|grep DFSFtpServer |grep -v grep | awk '{print $2}' | xargs kill ")
        print 'kill ftp status code: ', status
        print 'kill ftp output: ', output
        status,output = commands.getstatusoutput("rm  " + params.ftp_pid_dir)
        print 'remove ftp.pid status code: ', status
        print 'remove ftp.pid output: ', output
        print "********** Stop CTDFS_FTP Operation End **********"
    def start(self, env):
        import params
        env.set_params(params)
        print "********** Start CTDFS_FTP Operation Begin **********"        
        for filename in params.ctdfs_ftp_conf_filenames:
            file_path = params.ctdfs_conf_dir + '/' + filename
            print 'ctdfs_ftp_conf_filename = ', file_path
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            ftp_target_file_path = params.target_conf_dir + '/' + filename
            if not os.path.isfile(ftp_target_file_path):
                ln_cmd = 'ln -s ' + file_path + ' ' + ftp_target_file_path
                status,output = commands.getstatusoutput(ln_cmd)
                print 'Execute ln_cmd status code : ', status
                print 'Execute ln_cmd output : ', output
        status,output = commands.getstatusoutput("sudo -u " + params.superuser + " nohup sh " + params.start_ftp_dir + " > " + params.start_ftp_log_dir + " \&")
        print 'Execute start ftp status code: ', status
        print 'Execute start ftp output: ', output
        scripts_path = sys.path[0]
        target_ftp_pid = scripts_path + '/../ftp.pid'
        ln_pid_status,ln_pid_output = commands.getstatusoutput("ln -s " + params.ftp_pid_dir + " " + target_ftp_pid)
        Logger.info("ln_pid_status = " + str(ln_pid_status))
        Logger.info("ln_pid_output = " + ln_pid_output)
        #global REST_PID_DIR
        #FTP_PID_DIR = params.ftp_pid_dir
        #pid = format(FTP_PID_DIR)
        #print 'FTP_PID_DIR is ',FTP_PID_DIR
        #print 'pid is ', pid
        config = Script.get_config()
        Ftp.superuser = config['configurations']['dfs-site']['dfs.superuser']
        print "********** Start CTDFS_FTP Operation End **********"
    def status(self, env):
        #import params
        #env.set_params(params)
        print "********** Status CTDFS_FTP Operation Begin **********"
        #global FTP_PID_DIR 
        #pid = format(FTP_PID_DIR)
        user_infos=commands.getoutput("cat /etc/passwd|grep ^autodfs:")
        #user_infos=commands.getoutput("cat /etc/passwd|grep ^" + Ftp.superuser + ":")
        #user_infos=commands.getoutput("cat /etc/passwd|grep ^" + params.superuser + ":")
        user_root_path=user_infos.split(':')[5]
        #pid = format(user_root_path + "/ctdfs/pid/ftp.pid")
         
        scripts_path = sys.path[0]
        target_ftp_pid = scripts_path + '/../ftp.pid'
        pid = format(target_ftp_pid)
        check_process_status(pid)
        print "********** Status CTDFS_FTP Operation End **********"
    def configure(self, env):
        print "********** configure CTDFS_FTP Operation Begin **********"
        print "Do Nothing"
        print "********** configure CTDFS_FTP Operation End **********"     
if __name__ == "__main__":
    Ftp().execute()
