#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py" 

#mock origin
echo "Restart origin server"
python ${operation_file} stop_origin_server $config_sub_tag

