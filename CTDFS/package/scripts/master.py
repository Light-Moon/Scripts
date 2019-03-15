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
    def install(self, env):
        import params
        env.set_params(params)
        import kerberos
        print 'kerberos status is : ', kerberos.getKerberosStatus()
        print 'merge_keytabs_host is :', kerberos.getMergeKeytabsHost()
        print 'kerberos_principal is :', kerberos.getKerberosPrincipal()
        print 'kerberos_password is :', kerberos.getKerberosPassword()

        print '********** Install CTDFS_MASTER Operation Begin **********';
        print "Current superuser is [" + params.superuser + "]; Current supergroup is [" + params.supergroup + "]; Current install_package_path is [" + params.install_package_path + "]"
        status,output = commands.getstatusoutput("sh " + params.scripts_path + "/auto-deploy.sh -u " + params.superuser + " -g " + params.supergroup + " -p " + params.install_package_path + " -h " + kerberos.getMergeKeytabsHost() + " -i " + kerberos.getKerberosPrincipal() + " -k " + kerberos.getKerberosPassword() + " >> " + params.scripts_path + "/deploy.log 2>&1 ")
        print 'Execute auto-deploy.sh status code: ', status
        print 'Execute auto-deploy.sh output: ', output
        if status > 0:
            #exit();
            raise Exception("***********Execute auto-deploy.sh error!!!********", status)
        if not os.path.isdir(params.ctdfs_conf_dir):
            Directory([params.ctdfs_conf_dir],mode=0755,owner=params.superuser,group=params.supergroup,create_parents=True) 
        for filename in params.ctdfs_master_conf_filenames:
            file_path = params.ctdfs_conf_dir + '/' + filename
            print 'ctdfs_master_conf_filename = ', file_path
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
        status,output = commands.getstatusoutput("sh " + params.scripts_path + "/create-softlinks.sh " + params.target_conf_dir + " >> " + params.scripts_path + "/deploy.log 2>&1 ")				
        print 'create-softlinks status code:', status
        print 'create-softlinks output:', output
        #如果是合并keytab所在主机
        if kerberos.getKerberosStatus() == 'true':
            domain_name = commands.getoutput("hostname -f")
            if domain_name == kerberos.getMergeKeytabsHost():
                Logger.info("dfs.kerberos.enabled is true and this host is MergeKeytabsHost!")
                Logger.info("********** Initialization CTDFS Operation By Merge Keytab Begin **********")
                merge_keytab_status,merge_keytab_output = commands.getstatusoutput("sh " + params.scripts_path + "/merge_keytab.sh " + params.merge_cmds_file + " " + params.merge_keytabs_path + " " + params.merge_keytab_name + " " + params.ctdfs_keytab_path)
                Logger.info("merge_keytab_status = " + str(merge_keytab_status))
                Logger.info("merge_keytab_output = " + merge_keytab_output)
                if merge_keytab_status > 0:
                    #exit();
                    raise Exception("***********Execute merge keytab error!!!***********")
                chown_status,chown_output = commands.getstatusoutput("sudo chown " + params.superuser + ":" + params.supergroup + " " + params.merge_keytab)
                Logger.info("chown_status = " + str(chown_status))
                Logger.info("chown_output = " + chown_output)
                chmod_status,chmod_output = commands.getstatusoutput("sudo chmod " + " 644 " + params.merge_keytab)
                Logger.info("chmod_status = " + str(chmod_status))
                Logger.info("chmod_output = " + chmod_output)
                init_status,init_output = commands.getstatusoutput("sudo su - " + params.superuser + ' -c "' + params.ctdfs_cmd_dir + " -init " + params.merge_keytab + '"')
                Logger.info("init_status = " + str(init_status))
                Logger.info("init_output = " + init_output)
                if init_status > 0:
                    #exit();
                    raise Exception("***********Execute init merge keytab error!!!***********")
                Logger.info("********** Initialization CTDFS Operation By Merge Keytab End **********")
            else:
                Logger.info("dfs.kerberos.enabled = true ,but this host is not MergeKeytabsHost,so not to init CTDFS")
        else:
            Logger.info("********** Initialization CTDFS Operation By Example Keytab Begin **********")
            init_status,init_output = commands.getstatusoutput("sudo su - " + params.superuser + ' -c "' + params.ctdfs_cmd_dir + " -init " + params.ctdfs_default_keytab + '"')
            Logger.info("init_status = " + str(init_status))
            Logger.info("init_output = " + init_output)
            if init_status > 0:
                #exit();
                raise Exception("***********Execute init example keytab error!!!***********")
            Logger.info("********** Initialization CTDFS Operation By Example Keytab End **********")
        print '********** Install CTDFS_MASTER Operation End **********';
    def stop(self, env):
        print "********** Stop CTDFS_MASTER Operation Begin **********"
        print "Do Nothing"
        print "********** Stop CTDFS_MASTER Operation End **********"
    def start(self, env):
        import params
        env.set_params(params)
        print "********** Start CTDFS_MASTER Operation Begin **********"
        status,filenames = commands.getstatusoutput("find " + params.ctdfs_conf_dir + " -maxdepth 1 -name *.xml -o -name *.properties -type f")
        print 'find ctdfs_conf_filenames status code: ', status
        print 'find ctdfs_conf_filenames output: ', filenames
        for item in filenames.split('\n'):
            file_path = item
            print 'file_path=', file_path
            filename = item.split('/')[-1]
            prefix_filename = filename[:-4]
            print 'prefix_filename = ', prefix_filename
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
        status,output = commands.getstatusoutput("sh " + params.scripts_path + "/create-softlinks.sh " + params.target_conf_dir)			
        print 'create-softlinks status code:', status
        print 'create-softlinks output:', output
        # Logger.info(config['configurations']['dfs-site']['dfs.supergroup'])
        # Logger.info(config['configurations']['dfs-site'])
        print "********** Start CTDFS_MASTER Operation End **********"
    def status(self, env):
        #import params
        #env.set_params(params)
        print "********** Status CTDFS_MASTER Operation Begin **********"
        #pid =  format(params.master_pid_dir)
        #check_process_status(pid)
        status,pid = commands.getstatusoutput("ps -ef|grep NameNode |grep -v grep | awk '{print $2}'")
        if pid:
            raise ComponentIsNotRunning()
        print "********** Status CTDFS_MASTER Operation End **********"
    def configure(self, env):
        print "********** configure CTDFS_MASTER Operation Begin **********"
        print "Do Nothing"
        print "********** configure CTDFS_MASTER Operation End **********"
if __name__ == "__main__":
    Master().execute()
