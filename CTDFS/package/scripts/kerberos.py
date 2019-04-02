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
    cluster_security_authentication = config['configurations']['core-site']['hadoop.security.authentication']
    cluster_security_authorization = config['configurations']['core-site']['hadoop.security.authorization']
    #if cluster_security_authentication == 'kerberos' and str(cluster_security_authorization).lower() == 'true':
    if cluster_security_authentication == 'kerberos' and cluster_security_authorization == True:
        return 'true'
    else:
        return 'false'

def getMergeKeytabsHost():
    merge_keytabs_host = config['configurations']['ctdfs-kerberos-site']['dfs.merge.keytab.host']
    return merge_keytabs_host
	
def getKerberosPrincipal():
    kerberos_principal = config['configurations']['ctdfs-kerberos-site']['kadmin.local.principal']
    return kerberos_principal
	
def getKerberosPassword():
    kerberos_password = config['configurations']['ctdfs-kerberos-site']['kadmin.local.password']
    return kerberos_password

