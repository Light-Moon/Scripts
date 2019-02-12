#!/bin/bash
#If there is no args to specified, it will show usage.
if [ $# = 0 ]; then
	echo "Usage: $0 <conf_dir>"
	echo "Try '$0 --help' for more information."
elif [[ $# = 1 ]] && [[ $1 = '--help' ]]; then
	echo "*******************************start*********************************"
	echo "The shell script needs 1 parameter."
	echo "For Example: sh $0 /home/dfs/conf"
	echo "********************************end**********************************"
fi

#Make sure not end with a diagonal line
if [[ $1 = */ ]];then
	$1=${1%*/}
fi

#ctdfs_conf_dir=/var/lib/ambari-agent/cache/stacks/HDP/2.5/services/DFS_TEST/configuration
shell_script_path=`dirname "$0"`
target_conf_dir=$1
ctdfs_conf_dir=`cd ${shell_script_path}/../../configuration; pwd`
hdfs_conf_dir=/etc/hadoop/conf
hbase_conf_dir=/etc/hbase/conf
hdfs_conf_files=("core-site.xml" "hdfs-site.xml" "mapred-site.xml" "yarn-site.xml" "log4j.properties")
hbase_conf_file=hbase-site.xml

for hdfs_conf_file in "${hdfs_conf_files[@]}"
do
	if [ ! -f "${target_conf_dir}/${hdfs_conf_file}" ]; then
		`ln -s ${hdfs_conf_dir}/${hdfs_conf_file} ${target_conf_dir}/${hdfs_conf_file}`
	fi
done

if [ ! -f "${target_conf_dir}/${hbase_conf_file}" ]; then
	`ln -s ${hbase_conf_dir}/${hbase_conf_file} ${target_conf_dir}/${hbase_conf_file}`
fi
if [ ! -f "${target_conf_dir}/dfs-${hbase_conf_file}" ]; then
	`ln -s ${hbase_conf_dir}/${hbase_conf_file} ${target_conf_dir}/dfs-${hbase_conf_file}`
fi

#for ctdfs_conf_file in `find ${ctdfs_conf_dir} -maxdepth 1 -name '*.xml' -o -name '*.properties' -type f`
for ctdfs_conf_file in `find ${ctdfs_conf_dir} -maxdepth 1 -name '*.xml' -type f`
do
	file_name=${ctdfs_conf_file##*/}
	echo "ctdfs_conf_file is : [${file_name}]"
	#if [ "${file_name}" == "dfs-site.xml" ]; then
	#	`ln -s ${ctdfs_conf_file} ${target_conf_dir}/dfs-default.xml`
	#fi
	if [ ! -f "${target_conf_dir}/${file_name}" ]; then
		`ln -s ${ctdfs_conf_file} ${target_conf_dir}/${file_name}`
	fi
done
