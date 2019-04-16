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
        Logger.info("********** Install CTDFS_MASTER Operation Begin **********")
        print "Current superuser is [" + params.superuser + "]; Current supergroup is [" + params.supergroup + "]; Current install_package_path is [" + params.install_package_path + "]; kerberos status is [" + kerberos.getKerberosStatus() + "]; merge_keytabs_host is [" + kerberos.getMergeKeytabsHost() + "]; kerberos_principal is [" + kerberos.getKerberosPrincipal() + "]; kerberos_password is [" + kerberos.getKerberosPassword() + "]."
        auto_deploy_status,auto_deploy_output = commands.getstatusoutput("sh " + params.scripts_path + "/auto-deploy.sh -u " + params.superuser + " -g " + params.supergroup + " -p " + params.install_package_path + " -f " + kerberos.getKerberosStatus() + " -h " + kerberos.getMergeKeytabsHost() + " -i " + kerberos.getKerberosPrincipal() + " -k " + kerberos.getKerberosPassword() + " >> " + params.scripts_path + "/deploy.log 2>&1 ")
        Logger.info("auto_deploy_status = " + str(auto_deploy_status))
        Logger.info("auto_deploy_output = " + auto_deploy_output)
        if auto_deploy_status > 0:
            raise Exception("***********Execute auto-deploy.sh error!!!********", auto_deploy_status)
        if not os.path.isdir(params.ctdfs_conf_dir):
            Directory([params.ctdfs_conf_dir],mode=0755,owner=params.superuser,group=params.supergroup,create_parents=True) 
        for filename in params.ctdfs_master_conf_filenames:
            file_path = params.ctdfs_conf_dir + '/' + filename
            Logger.info("ctdfs_master_conf_filename = " + file_path)
            if not os.path.isfile(file_path):
                File([file_path],mode=0755,owner=params.superuser,group=params.supergroup)
            prefix_filename = filename[:-4]
            Logger.info("prefix_filename = " + prefix_filename)
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
        dependent_softlinks_status,dependent_softlinks_output = commands.getstatusoutput("sh " + params.scripts_path + "/dependent-softlinks.sh " + params.ctdfs_conf_dir + " >> " + params.scripts_path + "/deploy.log 2>&1 ")				
        Logger.info("dependent_softlinks_status = " + str(dependent_softlinks_status))
        Logger.info("dependent_softlinks_output = " + dependent_softlinks_output)
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
        Logger.info("********** Install CTDFS_MASTER Operation End **********")
    def stop(self, env):
        Logger.info("********** Stop CTDFS_MASTER Operation Begin **********")
        scripts_path = sys.path[0]
        master_pid = scripts_path + '/../../master.pid'
        #if not os.path.isfile(master_pid):
        fp = open(master_pid,'w')
        fp.write('False')
        fp.close()
        Logger.info("********** Stop CTDFS_MASTER Operation End **********")
    def start(self, env):
        import params
        env.set_params(params)
        Logger.info("********** Start CTDFS_MASTER Operation Begin **********")
        #status,filenames = commands.getstatusoutput("find " + params.ctdfs_conf_dir + " -maxdepth 1 -name *.xml -o -name *.properties -type f")
        find_conf_filenames_status,find_conf_filenames_output = commands.getstatusoutput("find " + params.ctdfs_conf_dir + " -maxdepth 1 -name *.xml -type f")
        Logger.info("find_conf_filenames_status = " + str(find_conf_filenames_status))
        Logger.info("find_conf_filenames_output = " + find_conf_filenames_output)
        for item in find_conf_filenames_output.split('\n'):
            file_path = item
            print 'file_path=', file_path
            filename = item.split('/')[-1]
            prefix_filename = filename[:-4]
            Logger.info("prefix_filename = " + prefix_filename)
            dict = params.config['configurations'][prefix_filename]
            write_xml(dict, file_path)
        dependent_softlinks_status,dependent_softlinks_output = commands.getstatusoutput("sh " + params.scripts_path + "/dependent-softlinks.sh " + params.ctdfs_conf_dir + " >> " + params.scripts_path + "/deploy.log 2>&1 ")
        Logger.info("dependent_softlinks_status = " + str(dependent_softlinks_status))
        Logger.info("dependent_softlinks_output = " + dependent_softlinks_output)
        if os.path.isdir(params.ambari_server_conf_dir):
            link_toAmbariServer_status,link_toAmbariServer_output = commands.getstatusoutput("sh " + params.scripts_path + "/ctdfs-softlinks.sh " + params.ctdfs_conf_dir + " " + params.ambari_server_conf_dir + " >> " + params.scripts_path + "/deploy.log 2>&1 ")
            Logger.info("link_toAmbariServer_status = " + str(link_toAmbariServer_status))
            Logger.info("link_toAmbariServer_output = " + link_toAmbariServer_output)
        scripts_path = sys.path[0]
        master_pid = scripts_path + '/../../master.pid'
        #if not os.path.isfile(master_pid):
        fp = open(master_pid,'w')
        fp.write('True')
        fp.close()
        Logger.info("********** Start CTDFS_MASTER Operation End **********")
    def status(self, env):
        Logger.info("********** Status CTDFS_MASTER Operation Begin **********")
        scripts_path = sys.path[0]
        master_pid = scripts_path + '/../../master.pid'
        MASTER_STATE = open(master_pid).read()
        if str(MASTER_STATE).lower() != 'true':
            #if open(master_pid).read() != True:
            raise ComponentIsNotRunning()
        Logger.info("********** Status CTDFS_MASTER Operation End **********")
    def configure(self, env):
        Logger.info("********** configure CTDFS_MASTER Operation Begin **********")
        Logger.info("Do Nothing")
        Logger.info("********** configure CTDFS_MASTER Operation End **********")
    def kerberizectdfs(self, env):
        import params
        env.set_params(params)
        import kerberos
        domain_name=commands.getoutput("hostname -f")
        keytab_name=params.superuser + '.' + domain_name + '.keytab'
        #每台机器生成keytab并进行kinit认证
        if kerberos.getKerberosStatus() == 'true':
            Logger.info("********** Regenerate keytab and Kinit host authentication and Init ctdfs component **********")
            kerberos_status,kerberos_output = commands.getstatusoutput("sh " + params.scripts_path + "/kerberos.sh " + params.superuser + " " + params.supergroup + " " + kerberos.getKerberosPrincipal() + " " + kerberos.getKerberosPassword() + " " + params.default_keytab_path + " >> " + params.scripts_path + "/kerberos.log 2>&1 ")
            Logger.info("kerberos_status = " + str(kerberos_status))
            Logger.info("kerberos_output = " + kerberos_output)
            if kerberos_status > 0:
                raise Exception("***********Execute kerberos.sh error!!!***********")
            #传输keytab到一台机器
            if kerberos.getMergeKeytabsHost() == domain_name:
                cpkeytab_status,cpkeytab_output = commands.getstatusoutput("cp " + params.default_keytab_path + "/" + keytab_name + " " + params.user_root_path + "/" + params.component_folder_name + "/keytab/merge")
                Logger.info("cpkeytab_status = " + str(cpkeytab_status))
                Logger.info("cpkeytab_output = " + cpkeytab_output)
            else:
                scpkeytab_status,scpkeytab_output = commands.getstatusoutput("scp " + params.default_keytab_path + "/" + keytab_name + " " + params.superuser + "@" + kerberos.getMergeKeytabsHost() + ":" + params.user_root_path + "/" + params.component_folder_name + "/keytab/merge")
                Logger.info("scpkeytab_status = " + str(scpkeytab_status))
                Logger.info("scpkeytab_output = " + scpkeytab_output)
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
