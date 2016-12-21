#!/bin/sh

cur_dir=`(cd "$(dirname "$0")"; pwd)`

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

python ${cur_dir}/vex_operation.py stop_redis_service $config_sub_tag
python ${cur_dir}/vex_operation.py rm_redis_cached_file $config_sub_tag
python ${cur_dir}/vex_operation.py start_redis_service $config_sub_tag
