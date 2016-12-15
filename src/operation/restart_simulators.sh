#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py"

basic_component_stop_commands=(
stop_ads_simulator
stop_content_router_simulator
stop_cns_simulator
stop_origin_server
)

basic_component_start_commands=(
start_ads_simulator
start_content_router_simulator
start_cns_simulator
start_origin_server
)

perf_component_stop_commands=(
batch_stop_origin_proxy_simulator
stop_origin_simulator
stop_cdvr_simulator
stop_vod_simulator
)

perf_component_start_commands=(
batch_start_origin_proxy_simulator
start_origin_simulator
start_cdvr_simulator
start_vod_simulator
)

perf_component_setup_content_commands=(
setup_ads_simulator_response_template
setup_content_router_ad_redirect_rule
setup_cdvr_simulator_ad_insertion
setup_vod_simulator_ad_insertion
setup_linear_ad_insertion
)

function operation(){
    local components=($*)
	echo ${components[*]}
	
	for dc in ${!components[@]}
    do
    {  
        echo "Execute operation: ${components[$dc]}"
        python ${operation_file} ${components[$dc]} $config_sub_tag
    }&
    done
    wait
    echo "Finish to do operation for: $components"
    sleep 1s
}

operation ${basic_component_stop_commands[@]}
operation ${basic_component_start_commands[@]}

operation ${perf_component_stop_commands[@]}
operation ${perf_component_start_commands[@]}

sleep 30s
operation ${perf_component_setup_content_commands[@]}
echo 'Finish to start all the simulators'















#older
#ads
#python ${operation_file} stop_ads_simulator $config_sub_tag
#python ${operation_file} start_ads_simulator $config_sub_tag
#python ${operation_file} setup_ads_simulator_response_template $config_sub_tag

#content router
#python ${operation_file} stop_content_router_simulator $config_sub_tag
#python ${operation_file} start_content_router_simulator $config_sub_tag
#python ${operation_file} setup_content_router_ad_redirect_rule $config_sub_tag

#cns
#python ${operation_file} stop_cns_simulator $config_sub_tag
#python ${operation_file} start_cns_simulator $config_sub_tag

#mock origin
#echo "Restart origin server"
#python ${operation_file} stop_origin_server $config_sub_tag
#python ${operation_file} start_origin_server $config_sub_tag

#origin proxy 
#python ${operation_file} batch_stop_origin_proxy_simulator $config_sub_tag
#python ${operation_file} batch_start_origin_proxy_simulator $config_sub_tag

#origin_simulator
#python ${operation_file} stop_origin_simulator $config_sub_tag
#python ${operation_file} start_origin_simulator $config_sub_tag

#cdvr simulator
#python ${operation_file} stop_cdvr_simulator $config_sub_tag
#python ${operation_file} start_cdvr_simulator $config_sub_tag
#python ${operation_file} setup_cdvr_simulator_ad_insertion $config_sub_tag

#vod simulator
#python ${operation_file} stop_vod_simulator $config_sub_tag
#python ${operation_file} start_vod_simulator $config_sub_tag
#python ${operation_file} setup_vod_simulator_ad_insertion $config_sub_tag

# linear ad insertion
#python ${operation_file} setup_linear_ad_insertion $config_sub_tag

