#coding=utf-8
import sys,os
import commands
from resource_management import *
from resource_management.libraries.script.script import Script

def getKerberosInfo(param):
    config = Script.get_config()
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
	
if __name__ == "__main__":
    getKerberosInfo()