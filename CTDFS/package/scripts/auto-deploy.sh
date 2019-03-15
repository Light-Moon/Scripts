#!/bin/bash
#首先要把ctdfs的安装包手动上传到hdfs指定目录

#If there is no args to specified, it will show usage.
if [ $# = 0 ]; then
	echo "Usage: $0 [-u <username>] [-g <groupname>] [-p <install_package_path>]"
	echo "Try '$0 --help' for more information."
	exit 0
elif [[ $# = 1 ]] && [[ $1 = '--help' ]]; then
	echo "*******************************start*********************************"
	echo "The number of parameters can be zero or more!Default values of parameters are:"
	echo "username : [${superuser}]"
	echo "groupname : [${supergroup}]"
	echo "install_package_path : [${install_package_path}]"
	echo "$0 [-u <username>]  -->  set only username , others take default values."
	echo "$0 [-u <groupname>]  -->  set only groupname , others take default values."
	echo "$0 [-u <install_package_path>]  -->  set only install_package_path , others take default values."
	echo "$0 [-u <username>] [-u <groupname>]  -->  set two parameters , install_package_path take default values."
	echo "and so on ..."
	echo "********************************end**********************************"
	exit 0
fi

#TODO:格式正确性进一步判断
#Get arguments.
while getopts ":u:g:p:h:i:k:" opt
do
	case ${opt} in
	u)
		superuser=$OPTARG
		echo "superuser = [${superuser}]"
		;;
        g)
		supergroup=$OPTARG
		echo "supergroup = [${supergroup}]"
		;;
        p)
		install_package_path=$OPTARG
		compressed_package_name=${install_package_path##*/}
		echo "install_package_path = [${install_package_path}]"
		;;
	h)
		merge_keytabs_host=$OPTARG
		echo "merge_keytabs_host = [${merge_keytabs_host}]"
		;;
	i)
		kerberos_principal=$OPTARG
		echo "kerberos_principal = [${kerberos_principal}]"
		;;
	k)
		kerberos_password=$OPTARG
		echo "kerberos_password = [${kerberos_password}]"
		;;
        ?)
		echo "Unknown parameter error!"
		echo "Usage: $0 [-u <username>] [-g <groupname>] [-p <install_package_path>]"
		exit 1
		;;
	esac
done

component_folder_name=ctdfs
#compressed_package_name=ctdfs.tar.gz
compressed_package_name=${install_package_path##*/}
#shell_script_path=`dirname "$0"; pwd`
shell_script_path="$( cd "$(dirname "$0")" ; pwd -P )"
log_file=${shell_script_path}"/deploy.log"
echo "shell_script_path = [${shell_script_path}]"
########################################
#Step1: Configure supergroup and superuser for CTDFS in host
${shell_script_path}/user_config.sh -u ${superuser} -g ${supergroup}

########################################
#Step2: Get user_root_path infos and make sure the path exist.
superuser_infos=`cat /etc/passwd|grep ^${superuser}:`
substr=${superuser_infos##*::}
user_root_path=${substr%%:*}
echo "user_root_path = [${user_root_path}]"
#if [ ! -d "${user_root_path}" ]; then
#	mkdir ${user_root_path}
#	sudo chown ${superuser}:${superuser}  ${user_root_path}
#fi

########################################
#Step3: Configure kerberos for dfs user
#TODO: 后期可以将kerberos认证这一部分代码单独封装起来，3个参数即可。superuser  principal  password
domain_name=`hostname -f`
keytab_path='/etc/security/keytabs'
keytab_name=${superuser}'.'${domain_name}'.keytab'
kerberos_status="true"
echo "keytab_path = [${keytab_path}]"
echo "keytab_name = [${keytab_name}]"
echo "domain_name = [${domain_name}]"
echo "kerberos_status = [${kerberos_status}]"

if [ "${kerberos_status}" == "true" ]; then
	echo "********** Kerberos Authentication Operation Start **********"
	principal_log=`/usr/bin/kadmin -p ${kerberos_principal} -w ${kerberos_password} -q "ank -randkey ${superuser}/${domain_name}"`
	if [ $? -eq 0 ]; then
        	echo ${principal_log}
                echo "Generate kerberos_principal success!"
	else
      		echo ${principal_log}
		echo "Generate kerberos_principal fail!"
                exit 1
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
	`sudo su - ${superuser} -c "/usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${superuser}/${domain_name}"`
fi

########################################
#Step4: Download installer package from hadoop cluster and to decompression.

if [ -d "${user_root_path}/${component_folder_name}" ]; then
	`mv ${user_root_path}/${component_folder_name} ${user_root_path}/${component_folder_name}$(date +%Y%m%d%H%M%S)`
	if [ $? -eq 0 ]; then
		echo "Backup folder of ${component_folder_name} success!"
	fi
fi
`sudo su - ${superuser} -c "mkdir ${user_root_path}/${component_folder_name}"`
if [ -f "${user_root_path}/${compressed_package_name}" ]; then
	echo "Install package is existed , no need to download!"	
	#`rm ${user_root_path}/${compressed_package_name}`
else
	`sudo su - ${superuser} -c "hadoop fs -get ${install_package_path} ${user_root_path}"`
	if [ $? -eq 0 ]; then
		echo "Download install package success!"	
	else
		echo "Download install package fail and exit shell script execution now!"
		exit 1
	fi
fi
`sudo su - ${superuser} -c "tar -xvzf ${user_root_path}/${compressed_package_name} -C ${user_root_path}/${component_folder_name} --strip-components 1 > /dev/null "`
#`su - ${superuser} -c "tar -xvzf ${user_root_path}/${compressed_package_name} -C ${user_root_path}/${component_folder_name} --strip-components 1 "`
if [ $? -eq 0 ]; then
	echo "Decompression install package success!"
	`rm ${user_root_path}/${compressed_package_name}`
else
	echo "Decompression install package fail!"
        # exit 1
fi

if [ "${merge_keytabs_host}" == "${domain_name}" ]; then
	`cp ${keytab_path}/${keytab_name} ${user_root_path}/${component_folder_name}/keytab/merge`
else
	`scp ${keytab_path}/${keytab_name} ${superuser}@${merge_keytabs_host}:${user_root_path}/${component_folder_name}/keytab/merge`
fi

########################################
#Step5: Changed JAVA_HOME of ${ctdfs_path}/bin/config.sh

java_home=`cat /etc/profile | grep JAVA_HOME= | awk -F '=' '{print $2}'`
if [ $? -eq 0 ]
then
	echo "Analyze java_home success, it is : [${java_home}]!"
else
	echo "Analyze java_home fail!"
fi
`sed -i "s:JAVA_HOME=null:JAVA_HOME=\${java_home}:g" ${user_root_path}/${component_folder_name}/bin/config.sh`
if [ $? -eq 0 ]
then
	echo "Changed JAVA_HOME of \${ctdfs_path}/bin/config.sh success!"
else
	echo "Changed JAVA_HOME of \${ctdfs_path}/bin/config.sh fail!"
fi

########################################
#Step6: Create dfs namespace in hbase and empowerment

# 1)kinit for hbase
hbase_keytab_name="hbase.headless.keytab"
hbase_sub_principal=`klist -k ${keytab_path}/${hbase_keytab_name} | sed -n 4p | awk -F '[ @]+' '{print $3}'`
echo "hbase_sub_principal = [${hbase_sub_principal}]"
`sudo su - hbase -c "/usr/bin/kinit -k -t ${keytab_path}/${hbase_keytab_name} ${hbase_sub_principal}"`
if [ $? -eq 0 ]
then
	echo "HBase initialization success!"
else
	echo "HBase initialization fail!"
	exit 1
fi
# 2)create namespace and empowerment
namespace=${superuser}
echo "namespace = [${namespace}]"
echo "shell_script_path = [${shell_script_path}]"
sudo su - hbase <<EOF
sh ${shell_script_path}/hbase_namespace.sh ${namespace}
exit
EOF

########################################
#Step6: Initialize CTDFS Component 
#`su - ${superuser} -c "${user_root_path}/${component_folder_name}/bin/dfsadmin -init ${keytab_path}/${keytab_name}"`
#if [ $? -eq 0 ]
#then
#	echo "Component initialization success!"
#else
#	echo "Component initialization fail!"
#fi
echo "Execute auto-deploy.sh script done!"
