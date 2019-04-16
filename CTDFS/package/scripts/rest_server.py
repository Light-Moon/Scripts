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
    def install(self, env):
        import params
        env.set_params(params)
        Logger.info("********** Install CTDFS_REST Operation Begin **********")
        if not os.path.isdir(params.ctdfs_conf_dir):
            Directory([params.ctdfs_conf_dir],mode=0755,owner=params.superuser,group=params.supergroup,create_parents=True) 
        for filename in params.ctdfs_rest_conf_filenames:
            Logger.info("ctdfs_rest_conf_filename = " + filename)
            file_path = params.ctdfs_conf_dir + '/' + filename
            Logger.info("file_path = " + file_path)
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            else:
                Logger.info(file_path + " is exist!") 
            prefix_filename = filename[:-4]
            Logger.info("prefix_filename = " + prefix_filename)
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            if os.path.isdir(params.ambari_server_conf_dir):
                rest_target_file_path = params.ambari_server_conf_dir + '/' + filename
                if os.path.isfile(rest_target_file_path):
                    rm_server_config_status,rm_server_config_output = commands.getstatusoutput("rm " + rest_target_file_path)
                    Logger.info("rm_server_config_status = " + str(rm_server_config_status))
                    Logger.info("rm_server_config_output = " + rm_server_config_output)  
                ln_cmd = 'ln -s ' + file_path + ' ' + rest_target_file_path
                link_toAmbariServer_status,link_toAmbariServer_output = commands.getstatusoutput(ln_cmd)
                Logger.info("link_toAmbariServer_status = " + str(link_toAmbariServer_status))
                Logger.info("link_toAmbariServer_output = " + link_toAmbariServer_output) 
        Logger.info("********** Install CTDFS_REST Operation End **********")
    def stop(self, env):
        import params
        env.set_params(params)
        Logger.info("********** Stop CTDFS_REST Operation Begin **********")
        kill_rest_status,kill_rest_output = commands.getstatusoutput("cat " + params.rest_pid_dir + " | xargs kill ")
        Logger.info("kill_rest_status = " + str(kill_rest_status))
        Logger.info("kill_rest_output = " + kill_rest_output)
        scripts_path = sys.path[0]
        target_rest_pid = scripts_path + "/../../rest.pid"
        rm_target_rest_pid_status,rm_target_rest_pid_output = commands.getstatusoutput("rm " + target_rest_pid)
        Logger.info("rm_target_rest_pid_status = " + str(rm_target_rest_pid_status))
        Logger.info("rm_target_rest_pid_output = " + rm_target_rest_pid_output)
        Logger.info("********** Stop CTDFS_REST Operation End **********")
    def start(self, env):
        import params
        env.set_params(params)
        Logger.info("********** Start CTDFS_REST Operation Begin **********")
        for filename in params.ctdfs_rest_conf_filenames:
            file_path = params.ctdfs_conf_dir + '/' + filename
            Logger.info("ctdfs_rest_conf_filename = " + file_path)
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            prefix_filename = filename[:-4]
            Logger.info("prefix_filename = " + prefix_filename)
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
            if os.path.isdir(params.ambari_server_conf_dir):
                rest_target_file_path = params.ambari_server_conf_dir + '/' + filename
                if os.path.isfile(rest_target_file_path):
                    rm_server_config_status,rm_server_config_output = commands.getstatusoutput("rm " + rest_target_file_path)
                    Logger.info("rm_server_config_status = " + str(rm_server_config_status))
                    Logger.info("rm_server_config_output = " + rm_server_config_output)                   
                ln_cmd = 'ln -s ' + file_path + ' ' + rest_target_file_path
                link_toAmbariServer_status,link_toAmbariServer_output = commands.getstatusoutput(ln_cmd)
                Logger.info("link_toAmbariServer_status = " + str(link_toAmbariServer_status))
                Logger.info("link_toAmbariServer_output = " + link_toAmbariServer_output) 
        start_rest_status,start_rest_output = commands.getstatusoutput("sudo -u " + params.superuser + " nohup sh " + params.start_rest_dir + " > " + params.start_ftp_log_dir + " \&")
        Logger.info("start_rest_status = " + str(start_rest_status))
        Logger.info("start_rest_output = " + start_rest_output)
        scripts_path = sys.path[0]
        target_rest_pid = scripts_path + '/../../rest.pid'
        if not os.path.isfile(target_rest_pid):
            ln_target_rest_pid_status,ln_target_rest_pid_output = commands.getstatusoutput("ln -s " + params.rest_pid_dir + " " + target_rest_pid)
            Logger.info("ln_target_rest_pid_status = " + str(ln_target_rest_pid_status))
            Logger.info("ln_target_rest_pid_output = " + ln_target_rest_pid_output)
        Logger.info("********** Start CTDFS_REST Operation End **********")
    def status(self, env):
        Logger.info("********** Status CTDFS_REST Operation Begin **********")
        scripts_path = sys.path[0]
        target_rest_pid = scripts_path + '/../../rest.pid'
        check_process_status(target_rest_pid)
        Logger.info("********** Status CTDFS_REST Operation End **********")
    def configure(self, env):
        Logger.info("********** configure CTDFS_REST Operation Begin **********")
        Logger.info("Do Nothing")
        Logger.info("********** configure CTDFS_REST Operation End **********")
if __name__ == "__main__":
    Rest().execute()
