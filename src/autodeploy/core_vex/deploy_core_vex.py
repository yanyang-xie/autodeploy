# -*- coding=utf-8 -*-
# author: yanyang.xie@gmail.com
import os
import sys

from fabric.context_managers import settings, cd
from fabric.operations import run
from fabric.tasks import Task, execute

from autodeploy.deploy import VEXAutoDeployBase
from utility import fab_util


class DeployCoreVEX(VEXAutoDeployBase, Task):
    
    def __init__(self, config_file_name='config.properties', config_sub_folder='', log_file='/tmp/deloy.log'):
        super(DeployCoreVEX, self).__init__(config_file_name, config_sub_folder, log_file=log_file)
        
    # 非通用，每个是自己的
    def init_fab_roles(self, **kwargs):
        print 'Setup fabric roles (core vex and memcached server)'
        if not self.parameters.has_key('core.vex.server.list'):
            raise Exception('not found core vex server list configuration by "core.vex.server.list"')
        else:
            core_vex_server_list = [self.user + '@' + core_ip for core_ip in self.parameters.get('core.vex.server.list').split(',')]
            fab_util.setRoles('core_vex_server', core_vex_server_list)
    
    def update_remote_build(self):
        with settings(parallel=True, roles=['core_vex_server', ]):
            execute(self.upload_build_and_do_golden_script)
    
    def update_remote_conf(self):
        with settings(parallel=True, roles=['core_vex_server', ]):
            execute(self.upload_config_to_remote_tomcat)
            execute(self.update_configurations_in_remote_server)
    
    def update_configurations_in_remote_server(self):
        get_internal_ip_shell = '/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk "{print $2}" |tr -d "addr:"'
        output = run(get_internal_ip_shell, pty=False)
        internal_ip = output.split('Bcst')[0].replace('inet', '').strip()
        
        print 'update cluster.host to internal IP %s' % (internal_ip)
        with cd(self.tomcat_conf_dir):
            run("sed '/cluster.host=/s/localhost/%s/g' vex.properties > vex-tmp.properties" % (internal_ip), pty=False)
            run('mv vex-tmp.properties vex.properties')
            run('chown -R tomcat:tomcat ' + self.tomcat_conf_dir, pty=False)

if __name__ == '__main__':
    deploy_dir = '/tmp/deploy-core-vex'
    log_file = os.getcwd() + os.sep + 'logs' + os.sep + 'deploy-core.log'
    
    config_sub_folder = sys.argv[0] if len(sys.argv) > 1 else ''
    # config_sub_folder = 'perf'

    deploy = DeployCoreVEX(config_sub_folder=config_sub_folder, log_file=log_file)
    deploy.run(deploy_dir)
