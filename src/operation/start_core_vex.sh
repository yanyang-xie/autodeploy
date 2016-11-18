#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py" 

python ${operation_file} run_mongo_script $config_sub_tag
python ${operation_file} start_vex_fe_cluster $config_sub_tag
python ${operation_file} start_core_vex_cluster $config_sub_tag
python ${operation_file} start_vex_director_cluster $config_sub_tag
python ${operation_file} start_vex_origin_manager_cluster $config_sub_tag
python ${operation_file} start_memcached_cluster $config_sub_tag
