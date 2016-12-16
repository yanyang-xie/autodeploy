#!/bin/sh

# cmds is operation list which is defined in vex_operation.py
cmds=""
config_sub_folder=""
sleep_time=3

operation_file="`(cd "$(dirname "$0")"; pwd)`/vex_operation.py"
if [ ! -f $operation_file ]; then
    echo "Not found the operation scipt ${operation_file}"
    exit 1
fi

function read_opt() {
	sub_folder=""
	sleep_time="1s"
	cmds=""
	
	while getopts :f:s:c: opt; do
	    case $opt in
	        f) config_sub_folder="$OPTARG" ;;
	        s) sleep_time="$OPTARG" ;;
	        c) cmds="$OPTARG" ;;
	        \?) echo "Invalid param" ;;
	    esac
	done
	
	echo "Configuration sub folder: $config_sub_folder"
	echo "Command execution time gap:$sleep_time"
	echo "Command list:$cmds"
}

function operation(){
	OLD_IFS="$IFS"
	IFS=","
	cmd_list=($cmds)
	IFS="$OLD_IFS"
	for cmd in ${cmd_list[@]}
	do
	{
		echo "python ${operation_file} $cmd $config_sub_folder"
        python ${operation_file} $cmd $config_sub_folder
        
        if [[ $? != 0 ]];then
   	    	echo "Operation $cmd failed. ${ret}"
   	    	exit 1
   	    fi
   	    
   	    #echo "sleep ${sleep_time} before next operation cmd"
   	    sleep sleep_time
	}
	done
	wait
    echo "Finish to do operation: $cmd_list"
}

read_opt $@
operation