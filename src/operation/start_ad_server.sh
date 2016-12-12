#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py" 

#origin proxy 
python ${operation_file} batch_stop_origin_proxy_simulator $config_sub_tag
python ${operation_file} batch_start_origin_proxy_simulator $config_sub_tag

