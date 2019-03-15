#!/bin/bash
namespace=$1
check_result=`echo "describe_namespace '${namespace}'" | hbase shell -n |grep "Unknown namespace"`
echo ${check_result}
if [ ! ${check_result} ];then
        echo "Namespace of [${namespace}] is exist."
        exit 0
else
        echo "Namespace of [${namespace}] is not exist."
fi      
echo "********** Create and Grant Namespace Begin **********"
superuser=${namespace}
hbase shell <<EOF 
create_namespace '${namespace}'
grant '${superuser}', 'RWXCA', '@${namespace}'
quit    
EOF
echo "********** Create and Grant Namespace End **********"

