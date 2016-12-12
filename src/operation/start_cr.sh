#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py"

#content router
python ${operation_file} stop_content_router_simulator $config_sub_tag
python ${operation_file} start_content_router_simulator $config_sub_tag
python ${operation_file} setup_content_router_ad_redirect_rule $config_sub_tag

