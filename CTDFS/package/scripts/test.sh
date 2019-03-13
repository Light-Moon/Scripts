#!bin/bash
kerberos_status=`cd "/var/lib/ambari-agent/cache/stacks/HDP/2.5/services/CTDFS/package/scripts"; python -c 'import test; print test.start()'`
echo "****************${kerberos_status}**************"
if [ "${kerberos_status}" != "true" ] && [ "${kerberos_status}" != "false" ];then
        echo "Config item of dfs.kerberos.enabled is error! It must be 'true' or 'false'!"
        exit 1
fi
#`cd /var/lib/ambari-agent/cache/stacks/HDP/2.5/services/CTDFS/package/scripts`
cd /var/lib/ambari-agent/cache/stacks/HDP/2.5/services/CTDFS/package/scripts
testuser=`python -c 'import test; print test.end()'`
echo "********${testuser}*********"
