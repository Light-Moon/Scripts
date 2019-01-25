#!/bin/bash
bin=`dirname $0`
bin=`cd $bin; pwd`
echo $bin
nohup sh $bin/run.sh ftp >> $bin/../logs/ftp.log 2>&1 &
echo $! > $bin/../pid/ftp.pid
#jps | grep Service | awk '{print $1}' > ../pid/ftp.pid
