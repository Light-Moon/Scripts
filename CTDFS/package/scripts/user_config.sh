#!/bin/bash
#Default parameters value.
superuser=dfs
supergroup=dfs
user_root_path=/home/${superuser}

#If there is no args to specified, it will show usage.
if [ $# = 0 ]; then
        echo "Usage: $0 [-u <username>] [-g <groupname>]"
        echo "Try '$0 --help' for more information."
        exit 0
elif [[ $# = 1 ]] && [[ $1 = '--help' ]]; then
        echo "*******************************start*********************************"
        echo "The number of parameters can be one or two!Default values of parameters are:"
        echo "username : [${superuser}]"
        echo "groupname : [${supergroup}]"
        echo "$0 [-u <username>]  -->  set only username , groupname take default values."
        echo "$0 [-u <groupname>]  -->  set only groupname , username take default values."
        echo "$0 [-u <username>] [-u <groupname>]  -->  set both of username and groupname parameters."
        echo "********************************end**********************************"
        exit 0
fi

#TODO:格式正确性进一步判断
#Get arguments.
while getopts ":u:g:" opt
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
        ?)
                echo "Unknown parameter error!"
                echo "Usage: $0 [-u <username>] [-g <groupname>]"
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
        #substr=${superuser_infos##*::}
        #user_root_path=${substr%%:*}
        #echo "The root path of ${superuser} user is :[${user_root_path}]"
fi