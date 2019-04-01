#!/bin/bash
#If there is no args to specified, it will show usage.
if [ $# = 0 ]; then
	echo "Usage: $0 <source_conf_dir> <target_conf_dir>"
	echo "Try '$0 --help' for more information."
elif [[ $# = 1 ]] && [[ $1 = '--help' ]]; then
	echo "*******************************start*********************************"
	echo "The shell script needs 2 parameter."
	echo "For Example: sh $0 /home/dfs/ctdfs/conf /var/lib/ambari-server/resources/stacks/HDP/2.5/services/CTDFS/configuration"
	echo "********************************end**********************************"
fi

#Make sure not end with a diagonal line
if [[ $1 = */ ]];then
	$1=${1%*/}
fi
if [[ $2 = */ ]];then
	$2=${2%*/}
fi

source_conf_dir=$1
target_conf_dir=$2
for ctdfs_conf_file in `find ${source_conf_dir} -maxdepth 1 -name '*.xml' -type f`
do
	file_name=${ctdfs_conf_file##*/}
	echo "ctdfs_conf_file is : [${file_name}]"
	if [ -f "${target_conf_dir}/${file_name}" ]; then
	`rm ${target_conf_dir}/${file_name}`
	fi
	`ln -s ${ctdfs_conf_file} ${target_conf_dir}/${file_name}`
done

