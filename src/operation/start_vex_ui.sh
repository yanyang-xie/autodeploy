#!/bin/sh
cur_dir=`(cd "$(dirname "$0")"; pwd)`
config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py" 

python ${cur_dir}/vex_operation.py stop_core_vex_cluster $config_sub_tag
python ${cur_dir}/vex_operation.py start_core_vex_cluster $config_sub_tag
