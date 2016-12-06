#!/bin/sh

deploy_script_dir=""
deploy_script_dir=${deploy_script_dir:-`(cd "$(dirname "$0")"; pwd)`}
echo "Deployment Base Dir is: ${deploy_script_dir}"

deploy_config_sub_tag=
echo "Deployment configuration sub tag is: ${deploy_config_sub_tag}"

version=
hosts=

while getopts :f:v:H opt
do
    case $opt in
        f)  
            deploy_config_sub_tag="$OPTARG"
            ;;
        v)
            version="$OPTARG"
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
    for dc in ${!compontents[@]}
    do
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
       	    
       	    echo "python ${cmd}"
       	    
       	    python $cmd
       	    if [[ $? != 0 ]];then
       	    	echo "Deploy failed. ${ret}"
       	    	exit 2
       	    fi
        fi
        
        echo "Finish to deployment all the compontents."
    done
}

# deploy
do_deploy