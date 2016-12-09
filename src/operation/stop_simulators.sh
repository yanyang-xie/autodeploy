#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py" 

#ads
python ${operation_file} stop_ads_simulator $config_sub_tag

#content router
python ${operation_file} stop_content_router_simulator $config_sub_tag

#cns
python ${operation_file} stop_cns_simulator $config_sub_tag

#mock origin
echo "Restart origin server"
python ${operation_file} stop_origin_server $config_sub_tag

#origin proxy 
python ${operation_file} batch_stop_origin_proxy_simulator $config_sub_tag

#origin_simulator
python ${operation_file} stop_origin_simulator $config_sub_tag

#cdvr simulator
python ${operation_file} stop_cdvr_simulator $config_sub_tag

#vod simulator
python ${operation_file} stop_vod_simulator $config_sub_tag

