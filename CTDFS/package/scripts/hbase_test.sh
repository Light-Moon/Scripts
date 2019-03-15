#!/bin/bash
echo "start check!"
#`sudo su - hbase -s "/bin/bash /var/lib/ambari-agent/cache/stacks/HDP/2.5/services/CTDFS/package/scripts/hbase.sh autodfs"`
path="/var/lib/ambari-agent/cache/stacks/HDP/2.5/services/CTDFS/package/scripts"
#sh /var/lib/ambari-agent/cache/stacks/HDP/2.5/services/CTDFS/package/scripts/hbase.sh autodfs
sudo su - hbase <<EOF
sh ${path}/hbase_namespace.sh autodfs
exit
EOF


#`sudo su - hbase -c "mkdir zql.txt"`
echo "end check!"

