#!/bin/bash
#$1为merge_cmds.txt   $2为keytabs的路径 $3为合并后的keytab名字 $4为ctdfs组件keytab路径
merge_cmds_file=$1
merge_keytabs_path=$2
merge_keytab_name=$3
ctdfs_keytab_path=$4

function writeFile(){
	`:>${merge_cmds_file}`
	for keytabName in `ls ${merge_keytabs_path} | grep *.keytab`
	do
		line="rkt "${keytabName}
		echo ${line} >> ${merge_cmds_file}
	done
	echo "wkt "${merge_keytab_name} >> ${merge_cmds_file}
}

function readLine(){
	cat ${merge_cmds_file} | while read Line
	do
		echo $Line
	done
}

writeFile
cd ${merge_keytabs_path};ktutil - <<EOF
`readLine`
q
EOF
`mv ${merge_keytabs_path}/${merge_keytab_name} ${ctdfs_keytab_path}`
`rm ${merge_keytabs_path}/*.keytab`