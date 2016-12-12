#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py" 

#ads
python ${operation_file} stop_ads_simulator $config_sub_tag
python ${operation_file} start_ads_simulator $config_sub_tag
python ${operation_file} setup_ads_simulator_response_template $config_sub_tag

