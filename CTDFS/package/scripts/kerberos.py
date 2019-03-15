#coding=utf-8
import sys,os
import commands
from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger

config = Script.get_config()

def getKerberosStatus():
    kerberos_status = config['configurations']['ctdfs-kerberos-site']['dfs.kerberos.enabled']
    return str(kerberos_status).lower()

def getMergeKeytabsHost():
    merge_keytabs_host = config['configurations']['ctdfs-kerberos-site']['dfs.merge.keytab.host']
    return merge_keytabs_host
	
def getKerberosPrincipal():
    kerberos_principal = config['configurations']['ctdfs-kerberos-site']['kadmin.local.principal']
    return kerberos_principal
	
def getKerberosPassword():
    kerberos_password = config['configurations']['ctdfs-kerberos-site']['kadmin.local.password']
    return kerberos_password

