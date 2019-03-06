#coding=utf-8
import sys,os
import commands
from resource_management import *
from resource_management.libraries.script.script import Script

config = Script.get_config()
superuser = config['configurations']['dfs-site']['dfs.superuser']
supergroup = config['configurations']['dfs-site']['dfs.supergroup']
install_package_path = config['configurations']['dfs-site']['dfs.installpack.path']
scripts_path = sys.path[0]
ctdfs_conf_dir = scripts_path + '/../../configuration'
#current_path = os.getcwd()
#scripts_path = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/package/scripts'
#ctdfs_conf_dir = current_path + '/cache/stacks/HDP/2.5/services/DFS_TEST/configuration'
user_infos=commands.getoutput("cat /etc/passwd|grep ^" + superuser + ":")
user_root_path=user_infos.split(':')[5]
target_conf_dir = user_root_path + '/ctdfs/conf'
ctdfs_cmd_dir = user_root_path + '/ctdfs/bin/dfsadmin'
start_ftp_dir = user_root_path + '/ctdfs/bin/startFtp.sh'
start_rest_dir = user_root_path + '/ctdfs/bin/startRest.sh'
start_ftp_log_dir = user_root_path + '/ctdfs/logs/startFtp.log'
start_rest_log_dir = user_root_path + '/ctdfs/logs/startRest.log'
master_pid_dir = user_root_path + '/ctdfs/pid/master.pid'
ftp_pid_dir = user_root_path + '/ctdfs/pid/ftp.pid'
rest_pid_dir = user_root_path + '/ctdfs/pid/rest.pid'
keytab='/etc/security/keytabs/' + superuser + '.service.keytab'
ctdfs_master_conf_filenames = ['dfs-site.xml','dfs-default.xml']
ctdfs_ftp_conf_filenames = ['ctdfs-ambari-site.xml']
ctdfs_rest_conf_filenames = ['ctdfs-rest-site.xml']