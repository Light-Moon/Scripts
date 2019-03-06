#!/bin/bash
#$1为merge_cmds.txt   $2为keytabs的路径 $3为合并后的keytab名字
merge_cmds_file=$1
keytab_path=$2
merge_keytab_name=$3

function writeFile(){
	`:>${merge_cmds_file}`
	for keytabName in `ls ${keytab_path}`
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
cd ${keytab_path};ktutil - <<EOF
`readLine`
list
q
EOF
