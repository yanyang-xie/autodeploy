#!/bin/sh

config_sub_tag=""
config_sub_tag=${config_sub_tag:-$1}

python vex_operation.py stop_ecc_spark $config_sub_tag
python vex_operation.py start_ecc_spark $config_sub_tag
