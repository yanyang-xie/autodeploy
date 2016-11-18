#!/bin/sh

cur_dir=`(cd "$(dirname "$0")"; pwd)`

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

python ${cur_dir}/vex_operation.py stop_vex_fe_cluster $config_sub_tag
python ${cur_dir}/vex_operation.py stop_core_vex_cluster $config_sub_tag
python ${cur_dir}/vex_operation.py stop_vex_director_cluster $config_sub_tag
python ${cur_dir}/vex_operation.py stop_vex_origin_manager_cluster $config_sub_tag
python ${cur_dir}/vex_operation.py stop_memcached_cluster $config_sub_tag

python ${cur_dir}/vex_operation.py run_mongo_script $config_sub_tag
python ${cur_dir}/vex_operation.py start_vex_fe_cluster $config_sub_tag
python ${cur_dir}/vex_operation.py start_core_vex_cluster $config_sub_tag
python ${cur_dir}/vex_operation.py start_vex_director_cluster $config_sub_tag
python ${cur_dir}/vex_operation.py start_vex_origin_manager_cluster $config_sub_tag
python ${cur_dir}/vex_operation.py start_memcached_cluster $config_sub_tag
