#coding=utf-8
import sys,os
import commands
from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger
#import params

config = Script.get_config()

def getKerberosStatus():
    #config = Script.get_config()
    #kerberos_status = params.config['configurations']['ctdfs-kerberos-site']['dfs.kerberos.enabled']
    kerberos_status = config['configurations']['ctdfs-kerberos-site']['dfs.kerberos.enabled']
    return str(kerberos_status).lower()

def getMergeKeytabsHost():
    merge_keytabs_host = config['configurations']['ctdfs-kerberos-site']['dfs.merge.keytab.host']
    return merge_keytabs_host
	
def getKerberosPrincipal():
    kerberos_principal = config['configurations']['ctdfs-kerberos-site']['kadmin.local.principal']
    return kerberos_principal
	
def getKerberosPassword():
    kerberos_principal = config['configurations']['ctdfs-kerberos-site']['kadmin.local.password']
    return kerberos_password
	
#def getKeytabPath():
#    keytab_path = params.keytab_path
#    return keytab_path
	
#def getKeytabName():
#    keytab_name = params.keytab_name
#    return keytab_name
	
def getKerberosInfo(param):
    if param == 1:
        kerberos_principal = config['configurations']['ctdfs-kerberos-site']['kadmin.local.principal']
        #kerberos_principal=111
        #value1=`python -c 'import kerberos; print kerberos.getKerberosInfo(1)'`
        return kerberos_principal
    elif param == 2:
        kerberos_password = config['configurations']['ctdfs-kerberos-site']['kadmin.local.password']
        #kerberos_password = 222
        #value2=`python -c 'import kerberos; print kerberos.getKerberosInfo(2)'`
        return kerberos_password
