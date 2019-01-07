#!/bin/bash
user=dfs1
group=dfs1

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
