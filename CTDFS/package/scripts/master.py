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
        print '********** Install CTDFS_MASTER Operation Begin **********';
        print "Current superuser is [" + params.superuser + "]; Current supergroup is [" + params.supergroup + "]; Current install_package_path is [" + params.install_package_path + "]; kerberos status is [" + kerberos.getKerberosStatus() + "]; merge_keytabs_host is [" + kerberos.getMergeKeytabsHost() + "]; kerberos_principal is [" + kerberos.getKerberosPrincipal() + "]; kerberos_password is [" + kerberos.getKerberosPassword() + "]."
        status,output = commands.getstatusoutput("sh " + params.scripts_path + "/auto-deploy.sh -u " + params.superuser + " -g " + params.supergroup + " -p " + params.install_package_path + " -f " + kerberos.getKerberosStatus() + " -h " + kerberos.getMergeKeytabsHost() + " -i " + kerberos.getKerberosPrincipal() + " -k " + kerberos.getKerberosPassword() + " >> " + params.scripts_path + "/deploy.log 2>&1 ")
        print 'Execute auto-deploy.sh status code: ', status
        print 'Execute auto-deploy.sh output: ', output
        if status > 0:
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
        status,output = commands.getstatusoutput("sh " + params.scripts_path + "/dependent-softlinks.sh " + params.ctdfs_conf_dir + " >> " + params.scripts_path + "/deploy.log 2>&1 ")				
        print 'create-softlinks status code:', status
        print 'create-softlinks output:', output
        if os.path.isdir(params.ambari_server_conf_dir):
            link_toAmbariServer_status,link_toAmbariServer_output = commands.getstatusoutput("sh " + params.scripts_path + "/ctdfs-softlinks.sh " + params.ctdfs_conf_dir + " " + params.ambari_server_conf_dir + " >> " + params.scripts_path + "/deploy.log 2>&1 ")
            Logger.info("link_toAmbariServer_status = " + str(link_toAmbariServer_status))
            Logger.info("link_toAmbariServer_output = " + link_toAmbariServer_output)
        if kerberos.getKerberosStatus() == 'true':
            domain_name = commands.getoutput("hostname -f")
            if domain_name == kerberos.getMergeKeytabsHost():
                Logger.info("dfs.kerberos.enabled is true and this host is MergeKeytabsHost!")
                Logger.info("********** Initialization CTDFS Operation By Merge Keytab Begin **********")
                merge_keytab_status,merge_keytab_output = commands.getstatusoutput("sh " + params.scripts_path + "/merge_keytab.sh " + params.merge_cmds_file + " " + params.merge_keytabs_path + " " + params.merge_keytab_name + " " + params.ctdfs_keytab_path)
                Logger.info("merge_keytab_status = " + str(merge_keytab_status))
                Logger.info("merge_keytab_output = " + merge_keytab_output)
                if merge_keytab_status > 0:
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
        #status,filenames = commands.getstatusoutput("find " + params.ctdfs_conf_dir + " -maxdepth 1 -name *.xml -o -name *.properties -type f")
        status,filenames = commands.getstatusoutput("find " + params.ctdfs_conf_dir + " -maxdepth 1 -name *.xml -type f")
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
        status,output = commands.getstatusoutput("sh " + params.scripts_path + "/dependent-softlinks.sh " + params.ctdfs_conf_dir + " >> " + params.scripts_path + "/deploy.log 2>&1 ")
        print 'create-softlinks status code:', status
        print 'create-softlinks output:', output
        if os.path.isdir(params.ambari_server_conf_dir):
            link_toAmbariServer_status,link_toAmbariServer_output = commands.getstatusoutput("sh " + params.scripts_path + "/ctdfs-softlinks.sh " + params.ctdfs_conf_dir + " " + params.ambari_server_conf_dir + " >> " + params.scripts_path + "/deploy.log 2>&1 ")
            Logger.info("link_toAmbariServer_status = " + str(link_toAmbariServer_status))
            Logger.info("link_toAmbariServer_output = " + link_toAmbariServer_output)
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
    def kerberizectdfs(self, env):
        import params
        env.set_params(params)
        import kerberos
        #TODO:可将部分变量统一定义在params.py中
        domain_name=commands.getoutput("hostname -f")
        component_folder_name='ctdfs'
        keytab_path='/etc/security/keytabs'
        keytab_name=params.superuser + '.' + domain_name + '.keytab'
       
        #每台机器生成keytab并进行kinit认证
        if kerberos.getKerberosStatus() == 'true':
            Logger.info("********** Regenerate keytab and Kinit host authentication and Init ctdfs component **********")
            kerberos_status,kerberos_output = commands.getstatusoutput("sh " + params.scripts_path + "/kerberos.sh " + params.superuser + " " + params.supergroup + " " + kerberos.getKerberosPrincipal() + " " + kerberos.getKerberosPassword() + " " + keytab_path + " >> " + params.scripts_path + "/kerberos.log 2>&1 ")
            Logger.info("kerberos_status = " + str(kerberos_status))
            Logger.info("kerberos_output = " + kerberos_output)
            if kerberos_status > 0:
                raise Exception("***********Execute kerberos.sh error!!!***********")
            #传输keytab到一台机器
            if kerberos.getMergeKeytabsHost() == domain_name:
                cpkeytab_status,cpkeytab_output = commands.getstatusoutput("cp " + keytab_path + "/" + keytab_name + " " + params.user_root_path + "/" + component_folder_name + "/keytab/merge")
                Logger.info("cpkeytab_status = " + str(cpkeytab_status))
                Logger.info("cpkeytab_output = " + cpkeytab_output)
                #`cp ${keytab_path}/${keytab_name} ${user_root_path}/${component_folder_name}/keytab/merge`
            else:
                scpkeytab_status,scpkeytab_output = commands.getstatusoutput("scp " + keytab_path + "/" + keytab_name + " " + params.superuser + "@" + kerberos.getMergeKeytabsHost() + ":" + params.user_root_path + "/" + component_folder_name + "/keytab/merge")
                Logger.info("scpkeytab_status = " + str(scpkeytab_status))
                Logger.info("scpkeytab_output = " + scpkeytab_output)
                #`scp ${keytab_path}/${keytab_name} ${superuser}@${merge_keytabs_host}:${user_root_path}/${component_folder_name}/keytab/merge`
            
            #合并keytab 
            if kerberos.getMergeKeytabsHost() == domain_name:
                merge_keytab_status,merge_keytab_output = commands.getstatusoutput("sh " + params.scripts_path + "/merge_keytab.sh " + params.merge_cmds_file + " " + params.merge_keytabs_path + " " + params.merge_keytab_name + " " + params.ctdfs_keytab_path)
                Logger.info("merge_keytab_status = " + str(merge_keytab_status))
                Logger.info("merge_keytab_output = " + merge_keytab_output)
                if merge_keytab_status > 0:
                    raise Exception("***********Execute merge keytab error!!!***********")
                chown_status,chown_output = commands.getstatusoutput("sudo chown " + params.superuser + ":" + params.supergroup + " " + params.merge_keytab)
                Logger.info("chown_status = " + str(chown_status))
                Logger.info("chown_output = " + chown_output)
                chmod_status,chmod_output = commands.getstatusoutput("sudo chmod " + " 644 " + params.merge_keytab)
                Logger.info("chmod_status = " + str(chmod_status))
                Logger.info("chmod_output = " + chmod_output)
                init_status,init_output = commands.getstatusoutput("sudo su - autodfs" + ' -c "' + params.ctdfs_cmd_dir + " -init " + params.merge_keytab + '"')
                Logger.info("init_status = " + str(init_status))
                Logger.info("init_output = " + init_output)
                if init_status > 0:
                    raise Exception("***********Execute init merge keytab error!!!***********")
                Logger.info("********** Initialization CTDFS Operation By Merge Keytab End **********")
        else:
            Logger.info("Cluster does not open Kerberos authentication function, so do nothing for this command!")
if __name__ == "__main__":
    Master().execute()
