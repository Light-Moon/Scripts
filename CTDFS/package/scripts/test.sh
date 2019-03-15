#!bin/bash
kerberos_principal="root/admin"
kerberos_password="admin"
superuser="autodfs"
domain_name=`hostname -f`
shell_script_path=`dirname "$0"; pwd`
log=`/usr/bin/kadmin -p ${kerberos_principal} -w ${kerberos_password} -q 'ank -randkey ${superuser}/${domain_name}'`
echo ${log}

keytab_path="/etc/security/keytabs"
keytab_name="autodfs.test.keytab"
#echo `/usr/bin/kadmin -p ${kerberos_principal} -w ${kerberos_password} -q 'xst -k /etc/security/keytabs/autodfs.test.keytab ${superuser}/${domain_name}'`
echo `/usr/bin/kadmin -p ${kerberos_principal} -w ${kerberos_password} -q "xst -k ${keytab_path}/${keytab_name} ${superuser}/${domain_name}"`

