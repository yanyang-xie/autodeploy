#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

#ads
python vex_operation.py stop_ads_simulator $config_sub_tag
python vex_operation.py start_ads_simulator $config_sub_tag
#python vex_operation.py setup_ads_simulator_response_template $config_sub_tag

#content router
python vex_operation.py stop_content_router_simulator $config_sub_tag
python vex_operation.py start_content_router_simulator $config_sub_tag
python vex_operation.py setup_content_router_ad_redirect_rule $config_sub_tag

#cns
python vex_operation.py stop_cns_simulator $config_sub_tag
python vex_operation.py start_cns_simulator $config_sub_tag

#mock origin
python vex_operation.py stop_content_router_simulator $config_sub_tag
python vex_operation.py start_content_router_simulator $config_sub_tag

#origin proxy 
#python vex_operation.py batch_stop_origin_proxy_simulator $config_sub_tag
#python vex_operation.py batch_start_origin_proxy_simulator $config_sub_tag

#origin_simulator
#python vex_operation.py stop_origin_simulator $config_sub_tag
#python vex_operation.py start_origin_simulator $config_sub_tag

#cdvr simulator
#python vex_operation.py stop_cdvr_simulator $config_sub_tag
#python vex_operation.py start_cdvr_simulator $config_sub_tag
#python vex_operation.py setup_cdvr_simulator_ad_insertion $config_sub_tag

#vod simulator
#python vex_operation.py stop_vod_simulator $config_sub_tag
#python vex_operation.py start_vod_simulator $config_sub_tag
#python vex_operation.py setup_vod_simulator_ad_insertion $config_sub_tag
