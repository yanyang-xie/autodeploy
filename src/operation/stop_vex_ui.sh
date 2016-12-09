#!/bin/sh

cur_dir=`(cd "$(dirname "$0")"; pwd)`

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

python ${cur_dir}/vex_operation.py stop_core_vex_cluster $config_sub_tag