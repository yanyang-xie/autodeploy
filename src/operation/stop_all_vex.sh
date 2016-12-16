#!/bin/sh

cur_dir=`(cd "$(dirname "$0")"; pwd)`

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

# All the supported compontents
declare -a compontents=()
compontents[1]="vex_fe_cluster"
compontents[2]="core_vex_cluster"
compontents[3]="vex_director_cluster"
compontents[4]="vex_origin_manager_cluster"
compontents[5]="memcached_cluster"

stop(){
    for c in ${!compontents[@]}
    do
    {
        echo ${compontents[$c]}
        python ${cur_dir}/vex_operation.py stop_${compontents[$c]} $config_sub_tag
        echo "Finish to stop ${compontents[$c]}"
    }&
    done
    wait
    echo 'Finish to stop all vex components'
}

stop
