#!/bin/bash
#If there is no args to specified, it will show usage.
if [ $# = 0 ]; then
	echo "Usage: $0 <ctdfs_conf_dir>"
	echo "Try '$0 --help' for more information."
elif [[ $# = 1 ]] && [[ $1 = '--help' ]]; then
	echo "*******************************start*********************************"
	echo "The shell script needs 1 parameter."
	echo "For Example: sh $0 /home/dfs/ctdfs/conf"
	echo "********************************end**********************************"
fi

#Make sure not end with a diagonal line
if [[ $1 = */ ]];then
	$1=${1%*/}
fi

target_conf_dir=$1
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

