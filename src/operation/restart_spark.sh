#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py"

python ${operation_file} stop_ecc_spark $config_sub_tag
python ${operation_file} start_ecc_spark $config_sub_tag
