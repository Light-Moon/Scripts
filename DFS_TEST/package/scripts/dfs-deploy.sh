#!/bin/bash
#首先要把ctdfs的安装包手动上传到hdfs指定目录上并利用hadoop fs -chown -R dfs:dfs /apps更改所属用户及组
#Default parameters value.
superuser=autodfs
supergroup=autodfs
keytab_path=/etc/security/keytabs
user_root_path=/home/${superuser}
component_folder_name=ctdfs
install_package_path=/apps/ctdfs.tar.gz
compressed_package_name=ctdfs.tar.gz

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
while getopts ":u:g:p:" opt
do
	case ${opt} in
	u)
		superuser=$OPTARG
		echo "superuser = [$superuser]"
		;;
        g)
		supergroup=$OPTARG
		echo "supergroup = [$supergroup]"
		;;
        p)
		install_package_path=$OPTARG
		compressed_package_name=${install_package_path##*/}
		echo "install_package_path = [$install_package_path]"
		;;
        ?)
		echo "Unknown parameter error!"
		echo "Usage: $0 [-u <username>] [-g <groupname>] [-p <install_package_path>]"
		exit 1
		;;
	esac
done


########################################
#Step1: Configure supergroup for CTDFS in host

egrep "^${supergroup}:" /etc/group > /dev/null 2>&1
if [ $? -ne 0 ]
then
	echo "Group of [${supergroup}] is not exist! Now to create ..."
    groupadd $supergroup
	if [ $? -ne 0 ]
	then
		echo "Create group of [${supergroup}] success!"
	fi
else
	echo "Group of ${supergroup} is existing! No need to create!"
fi

########################################
#Step2: Configure superuser for CTDFS in host

superuser_infos=`cat /etc/passwd|grep ^${superuser}:`
if [ -z "${superuser_infos}" ]; then
    echo "User of ${superuser} is not exist! Now to add user ..."
	useradd -g ${supergroup} -d ${user_root_path} -m ${superuser}
	if [ $? -ne 0 ]
	then
		echo "Add user of [${superuser}] success!"
	fi
	# read -p "please input password for ${superuser} user:" password	
	# echo ${password} |passwd --stdin ${superuser}	
else
    echo "User of ${superuser} is existing! No need to create!"
	#TODO: add ${superuser} to ${supergroup}
    substr=${superuser_infos##*::}
    user_root_path=${substr%%:*}
    echo "The root path of ${superuser} user is :[${user_root_path}]"
fi

########################################
#Step3: Configure kerberos for dfs user

kerberos_username=root/admin
kerberos_password=root
keytab_name=${superuser}.service.keytab
domain_name=`hostname -f`
echo "The domain_name is : [${domain_name}]"
#`/usr/bin/kadmin -p ${kerberos_username} -w ${kerberos_password} -q 'ank -randkey ${superuser}/${domain_name}'`
#`/usr/bin/kadmin -p ${kerberos_username} -w ${kerberos_password} -q 'xst -k ${keytab_path}/${keytab_name} ${superuser}/${domain_name}'`
#echo "0 0 * * * /usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${superuser}/${domain_name}" >> /var/spool/cron/${superuser}
#`crontab /var/spool/cron/${superuser}`
#`chown ${superuser}:${supergroup} /var/spool/cron/${superuser}`&&`chmod 644 /var/spool/cron/${superuser}`
#`chmod 644 ${keytab_path}/${keytab_name}`
echo "Current user is : [`whoami`]"
#`su - ${superuser} -c "/usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${superuser}/${domain_name}"`

########################################
#Step4: Read script parameters.
#	param1:Installation pack storage path in HDFS.

#if [ -n "$1" ]; then
#	${install_package_path}=$1
#	${compressed_package_name}=${1##*/}
#fi

########################################
#Step5: Download installer package from hadoop cluster and to decompression.

if [ -d "${user_root_path}/${component_folder_name}" ]; then
	`mv ${user_root_path}/${component_folder_name} ${user_root_path}/${component_folder_name}$(date +%Y%m%d%H%M%S)`
	if [ $? -eq 0 ]; then
		echo "Backup folder of ${component_folder_name} success!"
	fi
fi
`su - ${superuser} -c "mkdir ${user_root_path}/${component_folder_name}"`
if [ -f "${user_root_path}/${compressed_package_name}" ]; then
	#echo "Install package is existed , no need to download!"	
	`rm ${user_root_path}/${compressed_package_name}`
else
	`su - ${superuser} -c "hadoop fs -get ${install_package_path} ${user_root_path}"`
	if [ $? -eq 0 ]; then
		echo "Download install package success!"	
	else
		echo "Download install package fail and exit shell script execution now!"
		exit 1
	fi
fi
`su - ${superuser} -c "tar -xvzf ${user_root_path}/${compressed_package_name} -C ${user_root_path}/${component_folder_name} --strip-components 1 > /dev/null "`
if [ $? -eq 0 ]; then
	echo "Decompression install package success!"
	`rm ${user_root_path}/${compressed_package_name}`
else
	echo "Decompression install package fail!"
fi

########################################
#Step6: Changed JAVA_HOME of ${ctdfs_path}/bin/config.sh

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
#Step7: Create dfs namespace in hbase and empowerment

# 1)kinit for hbase
# hbase_keytab_name=hbase.headless.keytab
# hbase_sub_principal=klist -k ${keytab_path}/${hbase_keytab_name} | sed -n 4p | awk -F '[ @]+' '{print $3}'
# `su - hbase -c "/usr/bin/kinit -k -t ${keytab_path}/${hbase_keytab_name} hbase/${hbase_sub_principal}"`
# 2)create namespace and empowerment

########################################
#Step8: Create soft links for configuration files 单独拿出来了，因为配置文件不会自动从ambari-server传到agent上去，要自己先建立所有的配置文件
#shell_script_path=`dirname $0 | cd ; pwd`
#`sh ${shell_script_path}/create-softlinks.sh ${user_root_path} ${component_folder_name}`


########################################
#Step9: Initialize CTDFS Component 
`su - ${superuser} -c "${user_root_path}/${component_folder_name}/bin/dfsadmin -init ${keytab_path}/${keytab_name}"`
if [ $? -eq 0 ]
then
	echo "Component initialization success!"
else
	echo "Component initialization fail!"
fi
echo "Execute shell script done!"
