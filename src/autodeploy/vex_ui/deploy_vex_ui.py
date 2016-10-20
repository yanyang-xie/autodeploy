# -*- coding=utf-8 -*-
# author: yanyang.xie@gmail.com
import os
import sys

from fabric.context_managers import settings
from fabric.tasks import Task, execute

sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], "../.."))
from autodeploy.deploy import VEXAutoDeployBase
from utility import common_util

class DeployVEXUI(VEXAutoDeployBase, Task):

    def __init__(self, config_file_name='config.properties', config_sub_folder='', log_file='/tmp/deloy.log'):
        super(DeployVEXUI, self).__init__(config_file_name, config_sub_folder, log_file=log_file)
        self.server_config_name = 'vex.ui.server.list'
        self.server_role_name = 'vex_server'
        self.project_war_name = 'vex-ui'

    def init_fab_roles(self, **kwargs):
        print 'Setup fabric roles (vex ui)'
        if not self.parameters.has_key(self.server_config_name):
            raise Exception('not found vex ui server list configuration by %s' % (self.server_config_name))
        else:
            self.set_roles(self.server_role_name, self.server_config_name)

    def update_remote_build(self):
        with settings(parallel=True, roles=[self.server_role_name, ]):
            execute(self.upload_build_and_do_golden_script)

    def update_remote_conf(self):
        with settings(parallel=True, roles=[self.server_role_name, ]):
            execute(self.upload_config_to_remote_tomcat)

if __name__ == '__main__':
    deploy_dir = '/tmp/deploy-vex-ui'
    log_file = common_util.get_script_current_dir() + os.sep + 'logs' + os.sep + 'deploy-vex-ui.log'
    
    config_sub_folder = sys.argv[1] if len(sys.argv) > 1 else ''

    deploy = DeployVEXUI(config_sub_folder=config_sub_folder, log_file=log_file)
    deploy.run(deploy_dir)
