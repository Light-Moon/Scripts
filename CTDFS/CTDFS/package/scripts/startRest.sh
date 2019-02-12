#!/bin/bash
bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
nohup sh $bin/run.sh rest >> $bin/../logs/rest.log 2>&1 &
echo $! > $bin/../pid/rest.pid
#jps | grep Service | awk '{print $1}' > ../pid/rest.pid
