#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py"

python ${operation_file} stop_vex_origin_manager_cluster $config_sub_tag
