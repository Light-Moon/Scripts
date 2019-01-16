#!/bin/bash
#首先要把ctdfs的安装包手动上传到hdfs指定目录上并利用hadoop fs -chown -R dfs:dfs /apps更改所属用户及组
#Default parameters value.
superuser=autodfs
supergroup=autodfs
keytab_path=/etc/security/keytabs
user_root_path=/home/${superuser}
component_name=ctdfs
install_package_path=/apps/ctdfs.tar.gz
compressed_package_name=ctdfs.tar.gz

#If there is no args to specified, it will show usage.
if [ $# = 0 ]; then
	echo "Usage: $0 [-u <username>] [-g <groupname>] [-p <install_package_path>]"
	echo "Try '$0 --help' for more information."
fi

if [[ $# = 1 ]] && [[ $1 = '--help' ]]; then
	echo "*******************************start***********************************"
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
fi

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
			echo "install_package_path = [$install_package_path]"
			;;
        ?)
			echo "Unknown parameter error!"
			echo "Usage: $0 [-u <username>] [-g <groupname>] [-p <install_package_path>]"
			exit 1
			;;
    esac
done
