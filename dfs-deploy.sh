#!/bin/bash
user=dfs1
group=dfs1
keytab_path=/etc/security/keytabs

#create group if not exists
egrep "^${group}:" /etc/group >& /dev/null
if [ $? -ne 0 ]
then
	echo "group of ${group} is not exist!"
    groupadd $group
else
	echo "group of ${group} is exist!"
fi

#create user if not exists
user_infos=`cat /etc/passwd|grep ^${user}:`
echo ${user_infos}
user_root_path=/home/${user}
if [ -z "${user_infos}" ]; then
    echo "user of ${user} is not exist!"
	useradd -g ${group} -d ${user_root_path} -m ${user}
	read -p "please input password for ${user} user:" password	
	echo ${password} |passwd --stdin ${user}	
else
    echo "user of ${user} is exist!"
	#TODO: add ${user} to ${group}
    substr=${user_infos##*::}
    echo "substr:[${substr}]"
    user_root_path=${substr%%:*}
    echo "user_root_path:[${user_root_path}]"
fi

#config kerberos for dfs and get installer package from hadoop
kerberos_username=hbase/admin
kerberos_password=root
keytab_name=${user}.service.keytab
package_name=ctdfs
package_hdfs_path=/apps/dfs
domain_name=`hostname -f`
`/usr/bin/kadmin -p ${kerberos_username} -w ${kerberos_password} -q 'ank -randkey ${user}/${domain_name}'`
`/usr/bin/kadmin -p ${kerberos_username} -w ${kerberos_password} -q 'xst -k ${keytab_path}/${keytab_name} ${user}/${domain_name}'
echo "0 0 * * * /usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${user}/${domain_name}" >>/var/spool/cron/${user}
`crontab /var/spool/cron/${user}`
`chown ${user}:${user} /var/spool/cron/${user}`&&`chmod 644 /var/spool/cron/${user}`
`chmod 644 ${keytab_path}/${keytab_name}`
`su ${user}`
`/usr/bin/kinit -k -t ${keytab_path}/${keytab_name} ${user}/${domain_name}`
`hadoop fs -get ${package_hdfs_path}/${package_name} ${user_root_path}`
if [ ${user} == `whoami`]; then
	`exit`
fi


#TODO:在hbase上建立dfs命名空间并为dfs用户分配管理权限
#kinit for hbase
hbase_keytab_name=hbase.headless.keytab
hbase_sub_principal=klist -k ${keytab_path}/${hbase_keytab_name} | sed -n 4p | awk -F '[ @]+' '{print $3}'
`/usr/bin/kinit -k -t ${keytab_path}/${hbase_keytab_name} hbase/${hbase_sub_principal}`

#TODO:加上def start部分读配置并写入文件的内容

#TODO:建立软连接模块

#TODO:修改run.sh config.sh配置文件
java_home=echo `which java` | xargs ls -l | awk -F '->' '{print $2}' | xargs ls -l | awk -F '->' '{print $2}' | awk -F '/bin' '{print $1}'
#因路径中有/和默认分隔符冲突故自定义分隔符
sed -i 's:JAVA_HOME=null:JAVA_HOME=${java_home}:g' ${user_root_path}/${package_name}/conf/config.sh

#TODO:dfsadmin -init xxx.keytab


#部署完成