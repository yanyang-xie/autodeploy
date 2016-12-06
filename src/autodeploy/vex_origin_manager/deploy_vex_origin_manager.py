# -*- coding=utf-8 -*-
# author: yanyang.xie@gmail.com
import os
import sys
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], "../.."))

from fabric.context_managers import settings
from fabric.tasks import Task, execute

from autodeploy.deploy import VEXAutoDeployBase
from utility import common_util

class DeployVEXOriginManager(VEXAutoDeployBase, Task):

    def __init__(self, config_file_name='config.properties', log_file='/tmp/deloy.log'):
        super(DeployVEXOriginManager, self).__init__(config_file_name, log_file=log_file)
        self.server_config_name = 'vex.origin.manager.server.list'
        self.server_role_name = 'vex_server'
        self.project_war_name = 'vex-origin-manager'

    '''
    def init_fab_roles(self, **kwargs):
        print 'Setup fabric roles (vex origin manager)'
        if not self.parameters.has_key(self.server_config_name):
            raise Exception('not found vex origin manager server list configuration by %s' % (self.server_config_name))
        else:
            self.set_roles(self.server_role_name, self.server_config_name)
    '''

    def update_remote_build(self):
        with settings(parallel=True, roles=[self.server_role_name, ]):
            execute(self.upload_build_and_do_golden_script, run_golden_setup_script=self.run_golden_setup_script)

    def update_remote_conf(self):
        with settings(parallel=True, roles=[self.server_role_name, ]):
            execute(self.upload_config_to_remote_tomcat)

if __name__ == '__main__':
    deploy_dir = '/tmp/deploy-vex-origin-manager'
    log_file = common_util.get_script_current_dir() + os.sep + 'logs' + os.sep + 'deploy-vex-origin-manager.log'
    deploy = DeployVEXOriginManager(log_file=log_file)
    deploy.run(deploy_dir)
