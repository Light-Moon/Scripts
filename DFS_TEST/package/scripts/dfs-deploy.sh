#!/bin/bash
user=autodfs
group=autodfs
keytab_path=/etc/security/keytabs
user_root_path=/home/${user}
component_name=ctdfs
#TODO:首先要把ctdfs的安装包手动上传到hdfs指定目录上并利用hadoop fs -chown -R dfs:dfs /apps更改所属用户及组
default_package_path=/apps/ctdfs.tar.gz
default_compressed_package_name=ctdfs.tar.gz

########################################
#Step1: Configure group for CTDFS in host

egrep "^${group}:" /etc/group > /dev/null 2>&1
if [ $? -ne 0 ]
then
	echo "Group of [${group}] is not exist! Now to create ..."
    groupadd $group
	if [ $? -ne 0 ]
	then
		echo "Create group of [${group}] success!"
	fi
else
	echo "Group of ${group} is existing! No need to create!"
fi

########################################
#Step2: Configure user for CTDFS in host

user_infos=`cat /etc/passwd|grep ^${user}:`
if [ -z "${user_infos}" ]; then
    echo "User of ${user} is not exist! Now to add user ..."
	useradd -g ${group} -d ${user_root_path} -m ${user}
	if [ $? -ne 0 ]
	then
		echo "Add user of [${user}] success!"
	fi
	# read -p "please input password for ${user} user:" password	
	# echo ${password} |passwd --stdin ${user}	
else
    echo "User of ${user} is existing! No need to create!"
	#TODO: add ${user} to ${group}
    substr=${user_infos##*::}
    user_root_path=${substr%%:*}
    echo "The root path of ${user} user is :[${user_root_path}]"
fi

########################################
#Step3: Configure kerberos for dfs user

kerberos_username=root/admin
kerberos_password=root
keytab_name=${user}.service.keytab
domain_name=`hostname -f`
echo "The domain_name is : [${domain_name}]"
#`/usr/bin/kadmin -p ${kerberos_username} -w ${kerberos_password} -q 'ank -randkey ${user}/${domain_name}'`
#`/usr/bin/kadmin -p ${kerberos_username} -w ${kerberos_password} -q 'xst -k ${keytab_path}/${keytab_name} ${user}/${domain_name}'`
#echo "0 0 * * * /usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${user}/${domain_name}" >> /var/spool/cron/${user}
#`crontab /var/spool/cron/${user}`
#`chown ${user}:${user} /var/spool/cron/${user}`&&`chmod 644 /var/spool/cron/${user}`
#`chmod 644 ${keytab_path}/${keytab_name}`
echo "Current user is : [`whoami`]"
#`su - ${user} -c "/usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${user}/${domain_name}"`

########################################
#Step4: Read script parameters.
#	param1:Installation pack storage path in HDFS.

if [ -n "$1" ]; then
	${default_package_path}=$1
	${default_compressed_package_name}=${1##*/}
fi

########################################
#Step5: Download installer package from hadoop cluster and to decompression.

if [ -d "${user_root_path}/${component_name}" ]; then
	`mv ${user_root_path}/${component_name} ${user_root_path}/${component_name}$(date +%Y%m%d%H%M%S)`
	if [ $? -eq 0 ]; then
		echo "Backup folder of ${component_name} success!"
	fi
fi
`su - ${user} -c "mkdir ${user_root_path}/${component_name}"`
if [ -f "${user_root_path}/${default_compressed_package_name}"]; then
	echo "Install package is existed , no need to download!"	
else
	`su - ${user} -c "hadoop fs -get ${default_package_path} ${user_root_path}"`
	if [ $? -eq 0 ]; then
		echo "Download install package success!"
		`su - ${user} -c "tar -xvzf ${user_root_path}/${default_compressed_package_name} -C ${user_root_path}/${component_name} --strip-components 1 > /dev/null "`
	else
		echo "Download install package fail and exit shell script execution now!"
		exit
	fi
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
`sed -i 's:JAVA_HOME=null:JAVA_HOME="${java_home}":g' ${user_root_path}/${component_name}/bin/config.sh`
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
#Step8: Create soft links for configuration files

#dfs自身的配置文件并未读配置并更新写入文件，在master的启动模块统一更新
dfs_conf_dir=/var/lib/ambari-agent/cache/stacks/HDP/2.5/services/DFS_TEST/configuration
hdfs_conf_dir=/etc/hadoop/conf
hbase_conf_dir=/etc/hbase/conf
conf_dir=${user_root_path}/${component_name}/conf
hdfs_conf_files=("core-site.xml" "hdfs-site.xml" "mapred-site.xml" "yarn-site.xml" "log4j.properties")
hbase_conf_file=hbase-site.xml
for hdfs_conf_file in "${hdfs_conf_files[@]}"
do
	`ln -s ${hdfs_conf_dir}/${hdfs_conf_file} ${conf_dir}/${hdfs_conf_file}`
done
`ln -s ${hbase_conf_dir}/${hbase_conf_file} ${conf_dir}/${hbase_conf_file}`
`ln -s ${hbase_conf_dir}/${hbase_conf_file} ${conf_dir}/dfs-${hbase_conf_file}`
for dfs_conf_file in `find ${dfs_conf_dir} -maxdepth 1 -name '*.xml' -o -name '*.properties' -type f`
do
	file_name=${dfs_conf_file##*/}
	echo "dfs_conf_file is : [${file_name}]"
	#if [ "${file_name}" == "dfs-site.xml" ]; then
	#	`ln -s ${dfs_conf_file} ${conf_dir}/dfs-default.xml`
	#fi
	`ln -s ${dfs_conf_file} ${conf_dir}/${file_name}`
done

########################################
#Step9: Initialize CTDFS Component 

#dfsadmin -init xxx.keytab

echo "Execute shell script success!"
