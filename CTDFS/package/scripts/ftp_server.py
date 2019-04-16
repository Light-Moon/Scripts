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
    def install(self, env):
        import params
        env.set_params(params)
        Logger.info("********** Install CTDFS_FTP Operation Begin **********")
        if not os.path.isdir(params.ctdfs_conf_dir):
            Directory([params.ctdfs_conf_dir],mode=0755,owner=params.superuser,group=params.supergroup,create_parents=True)    
        for filename in params.ctdfs_ftp_conf_filenames:
            Logger.info("ctdfs_ftp_conf_filename = " + filename)
            file_path = params.ctdfs_conf_dir + '/' + filename
            Logger.info("file_path = " + file_path)
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            prefix_filename = filename[:-4]
            Logger.info("prefix_filename = " + prefix_filename)
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            if os.path.isdir(params.ambari_server_conf_dir):            
                ftp_target_file_path = params.ambari_server_conf_dir + '/' + filename
                if os.path.isfile(ftp_target_file_path):
                    rm_server_config_status,rm_server_config_output = commands.getstatusoutput("rm " + ftp_target_file_path)
                    Logger.info("rm_server_config_status = " + str(rm_server_config_status))
                    Logger.info("rm_server_config_output = " + rm_server_config_output)   
                ln_cmd = 'ln -s ' + file_path + ' ' + ftp_target_file_path
                link_toAmbariServer_status,link_toAmbariServer_output = commands.getstatusoutput(ln_cmd)
                Logger.info("link_toAmbariServer_status = " + str(link_toAmbariServer_status))
                Logger.info("link_toAmbariServer_output = " + link_toAmbariServer_output) 
        Logger.info("********** Install CTDFS_FTP Operation End **********")
    def stop(self, env):
        import params
        env.set_params(params)
        Logger.info("********** Stop CTDFS_FTP Operation Begin **********")
        kill_ftp_status,kill_ftp_output = commands.getstatusoutput("cat " + params.ftp_pid_dir + " | xargs kill ")
        Logger.info("kill_ftp_status = " + str(kill_ftp_status))
        Logger.info("kill_ftp_output = " + kill_ftp_output)
        scripts_path = sys.path[0]
        target_ftp_pid = scripts_path + "/../../ftp.pid"
        rm_target_ftp_pid_status,rm_target_ftp_pid_output = commands.getstatusoutput("rm " + target_ftp_pid)
        Logger.info("rm_target_ftp_pid_status = " + str(rm_target_ftp_pid_status))
        Logger.info("rm_target_ftp_pid_output = " + rm_target_ftp_pid_output) 
        Logger.info("********** Stop CTDFS_FTP Operation End **********")
    def start(self, env):
        import params
        env.set_params(params)
        Logger.info("********** Start CTDFS_FTP Operation Begin **********")
        for filename in params.ctdfs_ftp_conf_filenames:
            file_path = params.ctdfs_conf_dir + '/' + filename
            Logger.info("ctdfs_ftp_conf_filename = " + file_path)
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            prefix_filename = filename[:-4]
            Logger.info("prefix_filename = " + prefix_filename)
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            if os.path.isdir(params.ambari_server_conf_dir):
                ftp_target_file_path = params.ambari_server_conf_dir + '/' + filename
                if os.path.isfile(ftp_target_file_path):
                    rm_server_config_status,rm_server_config_output = commands.getstatusoutput("rm " + ftp_target_file_path)
                    Logger.info("rm_server_config_status = " + str(rm_server_config_status))
                    Logger.info("rm_server_config_output = " + rm_server_config_output)
                ln_cmd = 'ln -s ' + file_path + ' ' + ftp_target_file_path
                link_toAmbariServer_status,link_toAmbariServer_output = commands.getstatusoutput(ln_cmd)
                Logger.info("link_toAmbariServer_status = " + str(link_toAmbariServer_status))
                Logger.info("link_toAmbariServer_output = " + link_toAmbariServer_output)
        start_ftp_status,start_ftp_output = commands.getstatusoutput("sudo -u " + params.superuser + " nohup sh " + params.start_ftp_dir + " > " + params.start_ftp_log_dir + " \&")
        Logger.info("start_ftp_status = " + str(start_ftp_status))
        Logger.info("start_ftp_output = " + start_ftp_output)
        scripts_path = sys.path[0]
        target_ftp_pid = scripts_path + "/../../ftp.pid"
        if not os.path.isfile(target_ftp_pid):
            ln_target_ftp_pid_status,ln_target_ftp_pid_output = commands.getstatusoutput("ln -s " + params.ftp_pid_dir + " " + target_ftp_pid)
            Logger.info("ln_target_ftp_pid_status = " + str(ln_target_ftp_pid_status))
            Logger.info("ln_target_ftp_pid_output = " + ln_target_ftp_pid_output)
        Logger.info("********** Start CTDFS_FTP Operation End **********")
    def status(self, env):
        Logger.info("********** Status CTDFS_FTP Operation Begin **********")
        scripts_path = sys.path[0]
        target_ftp_pid = scripts_path + "/../../ftp.pid"
        pid = format(target_ftp_pid)
        check_process_status(pid)
        Logger.info("********** Status CTDFS_FTP Operation End **********")
    def configure(self, env):
        Logger.info("********** configure CTDFS_FTP Operation Begin **********")
        Logger.info("Do Nothing")
        Logger.info("********** configure CTDFS_FTP Operation End **********")  
if __name__ == "__main__":
    Ftp().execute()
