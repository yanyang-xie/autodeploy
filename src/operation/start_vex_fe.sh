#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py"

python ${cur_dir}/vex_operation.py start_vex_fe_cluster $config_sub_tag
