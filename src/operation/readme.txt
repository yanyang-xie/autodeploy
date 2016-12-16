Usage:
View task list:
# fab -f vex_operation.py --list

Run task:
python vex_operation.py task_name

Run task with config in subfolder, such as perf
python vex_operation.py task_name perf

Run multiple tasks
sh operation.sh -c "task1,task2" -f config_sub_folder -s time_gap_in_each_task