# autodeploy

1. autodeploy框架针对当前的VEX的各个组件的部署，提取出公共的基类。如下载build，更新build，更新配置文件。
2. 各个模块仅需要设置各自的远程hosts以及特殊的操作即可。
3. 框架默认会读取部署脚本当前目录下的config.properties作为基准参数。如果需要更多的参数，可以在运行run方法时传递。
4. 为了使同一模块，不同的环境(如performance, longevity, feature, production),运行同一套脚本， 可在部署脚本的目录下建立自己的配置文件的子目录。运行时，传入参数config_sub_folder='your config sub folder'

Command samples:
# python /your_dir/deploy_core_vex.py perf
