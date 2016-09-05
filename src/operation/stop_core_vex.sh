#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

python vex_operation.py stop_vex_fe_cluster $config_sub_tag
python vex_operation.py stop_core_vex_cluster $config_sub_tag
python vex_operation.py stop_vex_director_cluster $config_sub_tag
python vex_operation.py stop_vex_origin_manager_cluster $config_sub_tag
python vex_operation.py stop_memcached_cluster $config_sub_tag
