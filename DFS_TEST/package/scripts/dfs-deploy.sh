#!/bin/bash
user=autodfs
group=autodfs
keytab_path=/etc/security/keytabs
user_root_path=/home/${user}
component_name=ctdfs
#TODO:首先要把ctdfs的安装包上传到hdfs指定目录上并利用hadoop fs -chown -R dfs:dfs /apps更改所属用户及组
default_package_path=/apps/ctdfs.tar.gz
default_compressed_package_name=ctdfs.tar.gz
#create group if not exists
egrep "^${group}:" /etc/group >& /dev/null
if [ $? -ne 0 ]
then
	echo "Group of [${group}] is not exist! Now to create ..."
    groupadd $group
	if [ $? -ne 0 ]
	then
		echo "Create group of [${group}] success!"
	fi
else
	echo "group of ${group} is existing! No need to create!"
fi
#create user if not exists
user_infos=`cat /etc/passwd|grep ^${user}:`
echo ${user_infos}
if [ -z "${user_infos}" ]; then
    echo "user of ${user} is not exist! Now to add user ..."
	useradd -g ${group} -d ${user_root_path} -m ${user}
	if [ $? -ne 0 ]
	then
		echo "Add user of [${user}] success!"
	fi
	# read -p "please input password for ${user} user:" password	
	# echo ${password} |passwd --stdin ${user}	
else
    echo "user of ${user} is existing! No need to create!"
	#TODO: add ${user} to ${group}
    substr=${user_infos##*::}
    user_root_path=${substr%%:*}
    echo "The root path of ${user} user is :[${user_root_path}]"
fi
#判断是否带参数（安装包名）以及是否已存在安装的CTDFS.
if [ -n "$1" ]; then
	${default_package_path}=$1
	${default_compressed_package_name}=${1##*/}
fi
if [ -d "${user_root_path}/${component_name}" ]; then
	`mv ${user_root_path}/${component_name} ${user_root_path}/${component_name}$(date +%Y%m%d%H%M%S)`
fi
#config kerberos for dfs and get installer package from hadoop
kerberos_username=root/admin
kerberos_password=root
keytab_name=${user}.service.keytab
domain_name=`hostname -f`
echo "domain_name is : ${domain_name}"
#`/usr/bin/kadmin -p ${kerberos_username} -w ${kerberos_password} -q 'ank -randkey ${user}/${domain_name}'`
#`/usr/bin/kadmin -p ${kerberos_username} -w ${kerberos_password} -q 'xst -k ${keytab_path}/${keytab_name} ${user}/${domain_name}'`
#echo "0 0 * * * /usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${user}/${domain_name}" >> /var/spool/cron/${user}
#`crontab /var/spool/cron/${user}`
#`chown ${user}:${user} /var/spool/cron/${user}`&&`chmod 644 /var/spool/cron/${user}`
#`chmod 644 ${keytab_path}/${keytab_name}`
echo "current user is : `whoami`"
#`/usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${user}/${domain_name}`
`su - ${user} -c "hadoop fs -get ${default_package_path} ${user_root_path}"`
#`su - ${user}`
`su - ${user} -c "mkdir ${user_root_path}/${component_name}"`
if [ $? -eq 0 ]; then
    echo "download install package success!!!"
    `su - ${user} -c "tar -xvzf ${user_root_path}/${default_compressed_package_name} -C ${user_root_path}/${component_name} --strip-components 1"`
else
	echo "download ctdfs install package fail!!!"
	exit
fi

if [ "${user}" == `whoami` ]; then
	`exit`
fi
#TODO:在hbase上建立dfs命名空间并为dfs用户分配管理权限
#kinit for hbase
# hbase_keytab_name=hbase.headless.keytab
# hbase_sub_principal=klist -k ${keytab_path}/${hbase_keytab_name} | sed -n 4p | awk -F '[ @]+' '{print $3}'
# `/usr/bin/kinit -k -t ${keytab_path}/${hbase_keytab_name} hbase/${hbase_sub_principal}`
#TODO:加上def start部分读配置并写入文件的内容
#TODO:建立软连接模块


#TODO:修改run.sh config.sh配置文件
java_home=echo `which java` | xargs ls -l | awk -F '->' '{print $2}' | xargs ls -l | awk -F '->' '{print $2}' | awk -F '/bin' '{print $1}'
#因路径中有/和默认分隔符冲突故自定义分隔符
`sed -i 's:JAVA_HOME=null:JAVA_HOME=${java_home}:g' ${user_root_path}/${component_name}/bin/config.sh`
#TODO:dfsadmin -init xxx.keytab
#部署完成
echo "execute dfs-deploy.sh done!!!!"
