#!/bin/bash
echo "Usage: $0 [superuser] [supergroup] [principal] [password] [keytab_path]"
superuser=$1
supergroup=$2
kerberos_principal=$3
kerberos_password=$4
#keytab_path='/etc/security/keytabs'
keytab_path=$5
domain_name=`hostname -f`
keytab_name=${superuser}'.'${domain_name}'.keytab'

echo "********** Kerberos Authentication Operation Start **********"
principal_log=`/usr/bin/kadmin -p ${kerberos_principal} -w ${kerberos_password} -q "ank -randkey ${superuser}/${domain_name}"`
if [ $? -eq 0 ]; then
        echo ${principal_log}
        echo "Generate kerberos_principal success!"
else
        echo ${principal_log}
        echo "Generate kerberos_principal fail!(May be already exist!
)"
fi
if [ -f "${keytab_path}/${keytab_name}" ]; then
	#rm ${keytab_path}/${keytab_name}
	mv ${keytab_path}/${keytab_name} ${keytab_path}/${keytab_name}'.bak'
fi
keytab_log=`/usr/bin/kadmin -p ${kerberos_principal} -w ${kerberos_password} -q "xst -k ${keytab_path}/${keytab_name} ${superuser}/${domain_name}"`
if [ $? -eq 0 ]; then
        echo ${keytab_log} 
        echo "Generate kerberos_keytab success!"
else
        echo ${keytab_log}
        echo "Generate kerberos_keytab fail!"
        exit 1
fi
#echo "0 0 * * * /usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${superuser}/${domain_name}" >> /var/spool/cron/${superuser}
#`crontab /var/spool/cron/${superuser}`
#`chown ${superuser}:${supergroup} /var/spool/cron/${superuser}`&&`chmod 644 /var/spool/cron/${superuser}`
`sudo chown ${superuser}:${supergroup} ${keytab_path}/${keytab_name}`
`sudo chmod 644 ${keytab_path}/${keytab_name}`
echo "Current user is : [`whoami`]"
kinit_log=`sudo su - ${superuser} -c "/usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${superuser}/${domain_name}"`
if [ $? -eq 0 ]; then
        echo ${kinit_log}
        echo "Kinit success!"
else
        echo ${kinit_log}
        echo "Kinit fail!"
fi

