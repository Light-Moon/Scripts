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

class Rest(Script):
    REST_PID_DIR=''
    def install(self, env):
        import params
        env.set_params(params)
        print "********** Install CTDFS_REST Operation Begin **********" 
        if not os.path.isdir(params.ctdfs_conf_dir):
            Directory([params.ctdfs_conf_dir],mode=0755,owner=params.superuser,group=params.supergroup,create_parents=True) 
        for filename in params.ctdfs_rest_conf_filenames:
            print 'ctdfs_rest_conf_filename = ', filename
            file_path = params.ctdfs_conf_dir + '/' + filename
            print 'file_path = ', file_path
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            else:
                print file_path + ' is exist!' 
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            rest_target_file_path = params.target_conf_dir + '/' + filename
            if not os.path.isfile(rest_target_file_path):
                ln_cmd = 'ln -s ' + file_path + ' ' + rest_target_file_path
                status,output = commands.getstatusoutput(ln_cmd)
                print 'Execute ln_cmd status code : ', status
                print 'Execute ln_cmd output : ', output
            else:
                print rest_target_file_path + ' is exist!'
        print "********** Install CTDFS_REST Operation End **********" 
    def stop(self, env):
        import params
        env.set_params(params)
        print "********** Stop CTDFS_REST Operation Begin **********"         
        kill_rest_status,kill_rest_output = commands.getstatusoutput("cat " + params.rest_pid_dir + " | xargs kill ")
        Logger.info("kill_rest_status = " + str(kill_rest_status))
        Logger.info("kill_rest_output = " + kill_rest_output)
        print "********** Stop CTDFS_REST Operation End **********"
    def start(self, env):
        import params
        env.set_params(params)
        print "********** Start CTDFS_REST Operation Begin **********"        
        for filename in params.ctdfs_rest_conf_filenames:
            file_path = params.ctdfs_conf_dir + '/' + filename
            print 'ctdfs_rest_conf_filename = ', file_path
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            rest_target_file_path = params.target_conf_dir + '/' + filename
            if not os.path.isfile(rest_target_file_path):
                ln_cmd = 'ln -s ' + file_path + ' ' + rest_target_file_path
                status,output = commands.getstatusoutput(ln_cmd)
                print 'Execute ln_cmd status code : ', status
                print 'Execute ln_cmd output : ', output
        status,output = commands.getstatusoutput("sudo -u " + params.superuser + " nohup sh " + params.start_rest_dir + " > " + params.start_ftp_log_dir + " \&")
        print 'Execute start rest status code: ', status
        print 'Execute start rest output: ', output
        scripts_path = sys.path[0]
        target_rest_pid = scripts_path + '/../../rest.pid'
        ln_pid_status,ln_pid_output = commands.getstatusoutput("ln -s " + params.rest_pid_dir + " " + target_rest_pid)
        Logger.info("ln_pid_status = " + str(ln_pid_status))
        Logger.info("ln_pid_output = " + ln_pid_output)
        #global REST_PID_DIR
        #REST_PID_DIR = params.rest_pid_dir
        #pid = format(REST_PID_DIR)
        #print 'REST_PID_DIR is ',REST_PID_DIR
        #print 'pid is ', pid
        print "********** Start CTDFS_REST Operation End **********"
    def status(self, env):
        #import params
        #env.set_params(params)
        print "********** Status CTDFS_REST Operation Begin **********"
        #global REST_PID_DIR
        #pid = format(REST_PID_DIR)
        user_infos=commands.getoutput("cat /etc/passwd|grep ^autodfs:")
        #config = Script.get_config()
        #superuser = config['configurations']['dfs-site']['dfs.superuser']
        #user_infos=commands.getoutput("cat /etc/passwd|grep ^" + superuser + ":")      
        #user_infos=commands.getoutput("cat /etc/passwd|grep ^" + params.superuser + ":")
        user_root_path=user_infos.split(':')[5]
        #pid = format(user_root_path + "/ctdfs/pid/rest.pid")
         
        scripts_path = sys.path[0]
        target_rest_pid = scripts_path + '/../../rest.pid'
        check_process_status(target_rest_pid)
        print "********** Status CTDFS_REST Operation End **********"
    def configure(self, env):
        print "********** configure CTDFS_REST Operation Begin **********"
        print "Do Nothing"
        print "********** configure CTDFS_REST Operation End **********"     
if __name__ == "__main__":
    Rest().execute()
