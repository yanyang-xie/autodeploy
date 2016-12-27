#!/bin/sh

deploy_script_dir=""
deploy_script_dir=${deploy_script_dir:-`(cd "$(dirname "$0")"; pwd)`}
echo "Deployment Base Dir is: ${deploy_script_dir}"

deploy_config_sub_tag=
echo "Deployment configuration sub tag is: ${deploy_config_sub_tag}"

version=
hosts=
download=

while getopts :f:v:d:H: opt
do
    case $opt in
        f)  
            deploy_config_sub_tag="$OPTARG"
            ;;
        v)
            version="$OPTARG"
            ;;
        d)
            download="$OPTARG"
            ;;
        H)  
            hosts="$OPTARG"
            ;;
    esac
done

# All the supported compontents
declare -a compontents=()
compontents[1]="vex_ui/deploy_vex_ui.py"
compontents[2]="core_vex/deploy_core_vex.py"
compontents[3]="vex_fe/deploy_vex_fe.py"
compontents[4]="vex_director/deploy_vex_director.py"
compontents[5]="vex_origin_manager/deploy_vex_origin_manager.py"

do_deploy(){
    succeed=0;

    for dc in ${!compontents[@]}
    do
    {
    	deploy_scipt_file="${deploy_script_dir}/${compontents[$dc]}"
    	
    	if [ ! -f $deploy_scipt_file ]; then
            echo "Not found the deploy scipt ${deploy_scipt_file}"
            exit 1
        else
       	    cmd="${deploy_scipt_file}"
       	    if [ ! -f $deploy_config_sub_tag ];then
       	        cmd="${cmd} -f ${deploy_config_sub_tag}"
       	    fi
       	    
       	    if [ ! -f $version ];then
       	        cmd="${cmd} -v ${version}"
       	    fi
       	    
       	    if [ ! -f $hosts ];then
       	        cmd="${cmd} -H ${hosts}"
       	    fi
       	    
       	    if [ ! -f $download ];then
       	        cmd="${cmd} -d ${download}"
       	    fi
       	    
       	    echo "python ${cmd}"
       	    
       	    python $cmd
       	    if [[ $? != 0 ]];then
       	    	echo "Deploy failed. ${ret}"
       	    	succeed=-1;
       	    	exit 2
       	    fi
        fi
    }&
    done
    wait
    
    if [[ succeed == 0 ]];then
    	echo "Finish to deployment all the compontents."
    else
    	echo "Deploy failed for some components, please check log for details."
    fi
}

# deploy
do_deploy