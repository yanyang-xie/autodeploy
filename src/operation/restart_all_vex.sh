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

start(){
    for c in ${!compontents[@]}
    do
    {
        python ${cur_dir}/vex_operation.py start_${compontents[$c]} $config_sub_tag
        echo "Finish to start ${compontents[$c]}"
    }&
    done
    wait
    echo 'Finish to start all vex components'
}

mongo_clear(){
	python ${cur_dir}/vex_operation.py run_mongo_script $config_sub_tag
}

stop
sleep 3s

mongo_clear
start








#older
#python ${cur_dir}/vex_operation.py stop_vex_fe_cluster $config_sub_tag
#python ${cur_dir}/vex_operation.py stop_core_vex_cluster $config_sub_tag
#python ${cur_dir}/vex_operation.py stop_vex_director_cluster $config_sub_tag
#python ${cur_dir}/vex_operation.py stop_vex_origin_manager_cluster $config_sub_tag
#python ${cur_dir}/vex_operation.py stop_memcached_cluster $config_sub_tag

#python ${cur_dir}/vex_operation.py run_mongo_script $config_sub_tag
#python ${cur_dir}/vex_operation.py start_memcached_cluster $config_sub_tag
#python ${cur_dir}/vex_operation.py start_core_vex_cluster $config_sub_tag
#python ${cur_dir}/vex_operation.py start_vex_fe_cluster $config_sub_tag
#python ${cur_dir}/vex_operation.py start_vex_director_cluster $config_sub_tag
#python ${cur_dir}/vex_operation.py start_vex_origin_manager_cluster $config_sub_tag