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
if [[ $1 = */ ]];then
	$1=${1%*/}
fi
#dfs_conf_dir=/var/lib/ambari-agent/cache/stacks/HDP/2.5/services/DFS_TEST/configuration
shell_script_path=`dirname "$0"`
dfs_conf_dir=`cd ${shell_script_path}/../../configuration; pwd`
hdfs_conf_dir=/etc/hadoop/conf
hbase_conf_dir=/etc/hbase/conf
conf_dir=$1
hdfs_conf_files=("core-site.xml" "hdfs-site.xml" "mapred-site.xml" "yarn-site.xml" "log4j.properties")
hbase_conf_file=hbase-site.xml
for hdfs_conf_file in "${hdfs_conf_files[@]}"
do
	`ln -s ${hdfs_conf_dir}/${hdfs_conf_file} ${conf_dir}/${hdfs_conf_file}`
done
`ln -s ${hbase_conf_dir}/${hbase_conf_file} ${conf_dir}/${hbase_conf_file}`
`ln -s ${hbase_conf_dir}/${hbase_conf_file} ${conf_dir}/dfs-${hbase_conf_file}`
for dfs_conf_file in `find ${dfs_conf_dir} -maxdepth 1 -name '*.xml' -type f`
do
	file_name=${dfs_conf_file##*/}
	echo "dfs_conf_file is : [${file_name}]"
	#if [ "${file_name}" == "dfs-site.xml" ]; then
	#	`ln -s ${dfs_conf_file} ${conf_dir}/dfs-default.xml`
	#fi
	`ln -s ${dfs_conf_file} ${conf_dir}/${file_name}`
done