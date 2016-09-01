# -*- coding=utf-8 -*-
# author: yanyang.xie@gmail.com

import os
import string
import sys
import time

from fabric.colors import red
from fabric.context_managers import cd, settings, lcd
from fabric.operations import local, put, run
from fabric.state import env
from fabric.tasks import execute, Task
from fabric.utils import abort

from utility import common_util, log_util, fab_util, download_sona_build


class AutoDeployBase(object):
    '''
    Basic module for auto deployment
    '''

    def __init__(self, config_file, log_file='/tmp/deloy.log'):
        self.config_file = config_file
        self.log_file = log_file
        self.tomcat_dir = '/usr/local/thistech/tomcat/'
        self.tomcat_conf_dir = self.tomcat_dir + 'lib/'
        self.parameters = common_util.load_properties(self.config_file)
        
        self.auto_download_build = True
        self.user, self.public_key, self.password, self.golden_files = (None, None, None, None)
        self.sona_user_name, self.sona_user_password = (None, None)
        self.project_name, self.project_version, self.project_extension_name = (None, None, None)
        self.download_build_file_dir, self.downloaded_build_file_name, self.download_command_prefix = (None, None, None)
        self.http_proxy, self.https_proxy = (None, None)
    
    def init_log(self):
        log_file_dir = os.path.dirname(self.log_file) + os.sep
        log_file_name = self.log_file.split(os.sep)[-1]
        print 'Log file is %s' % (self.log_file)
        sys.stdout = log_util.Logger(log_file_dir, "%s.%s" % (log_file_name, time.strftime("%Y-%m-%d", time.localtime())))
        sys.stderr = sys.stdout
    
    def _has_attr(self, attr_name):
        if not hasattr(self, attr_name):
            return False
        else:
            return getattr(self, attr_name, None)
       
    def _set_attr(self, attr_name, attr_value):
        setattr(self, attr_name, attr_value)
    
class VEXAutoDeployBase(AutoDeployBase):
    def __init__(self, config_file, log_file='/tmp/deloy.log'):
        super(VEXAutoDeployBase, self).__init__(config_file, log_file)
    
    def init_configred_parameters(self):
        '''读取配置文件中的参数，并且将其设置为当前对象的属性'''
        print '#' * 100
        print 'Initial deplpy parameters from config file %s' % (self.config_file)
        set_attr = lambda attr_name, config_name, default_value = None: self._set_attr(attr_name, common_util.get_config_value_by_key(self.parameters, config_name, default_value))
        
        set_attr('user', 'user', 'root')
        set_attr('public_key', 'public.key')
        set_attr('password', 'password')
        set_attr('golden_files', 'golden.config.file.list')
        
        auto_download_build = common_util.get_config_value_by_key(self.parameters, 'auto.download.sona.build')
        if auto_download_build and string.lower(auto_download_build) == 'true':
            setattr(self, 'auto_download_build', True)
        else:
            setattr(self, 'auto_download_build', False)
        print 'auto_download_build:%s' % (self.auto_download_build)
        
        set_attr('sona_user_name', 'sona.user.name')
        set_attr('sona_user_password', 'sona.user.passwd')
        set_attr('project_name', 'project.name')
        set_attr('project_version', 'project.version')
        set_attr('project_extension_name', 'project.extension.name')
        
        set_attr('download_build_file_dir', 'build.local.file.dir', os.getcwd())
        set_attr('downloaded_build_file_name', 'build.local.file.name')
        set_attr('download_command_prefix', 'download.command.prefix')
        
        set_attr('http_proxy', 'http.proxy')
        set_attr('https_proxy', 'https.proxy')
        
        # check fabric ssh configurations
        if getattr(self, 'user') is None:
            raise Exception('Configuration for user is not set, please check')
        
        if getattr(self, 'public_key') is None and getattr(self, 'password') is None:
            raise Exception('Configuration for publick.key and password must have one of each, please check')
        
        if auto_download_build:
            check_sona_download_list = ['sona_user_name', 'sona_user_password', 'project_name',
                'project_version', 'project_extension_name', 'download_build_file_dir', 'downloaded_build_file_name', ]
            
            for att in check_sona_download_list:
                if getattr(self, att) is None:
                    raise Exception('Configuration for %s is not set, please check' % (att))
        
        else:
            if getattr(self, 'downloaded_build_file_name') is None:
                raise Exception('Configuration for %s is not set, please check' % ('build.local.file.name'))
    
    # 每个组件可以单独传入自己的kwargs. 但是通用的参数，这里应该明确写出来。比如deploy_dir
    def init_component_deploy_parameters(self, deploy_dir, **kwargs):
        self.deploy_dir = deploy_dir
        self.parameters.update(kwargs)
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def init_deploy_dir(self, deploy_dir='/tmp/deploy/'):
        if not self._has_attr('deploy_dir'):
            print red('deploy dir is not set')
            abort(2)
        
        print 'Initial deployment directory %s' % (self.deploy_dir)
        local('rm -rf ' + self.deploy_dir)
        local('mkdir -p ' + self.deploy_dir)
    
    # setup fabric SSH environments
    def init_fab_ssh_env(self):
        print 'Setup fabric ssh environment'
        if self.public_key is None and self.password is None:
            raise Exception('public.key or password must have one')
        
        if self.public_key:
            fab_util.setKeyFile(getattr(self, 'public_key'))
        
        if self.password:
            fab_util.setKeyFile(getattr(self, 'password'))
        
        if self.user:
            fab_util.set_user(getattr(self, 'user'))
    
    # 非通用
    def init_fab_roles(self, **kwargs):
        pass
    
    # 通用
    def download_build(self):
        print '#' * 100
        if self.auto_download_build:
            download_script = download_sona_build.__file__
            command = 'python %s -u %s -p %s -n %s -v %s -e %s -d %s -f %s' % (download_script, self.sona_user_name, self.sona_user_password, self.project_name, self.project_version, self.project_extension_name, self.download_build_file_dir, self.downloaded_build_file_name)
            command = command + ' -y %s ' % (self.http_proxy) if self.http_proxy is not None else command
            command = command + ' -Y %s ' % (self.https_proxy) if self.https_proxy is not None else command
            if self.download_command_prefix is not None:
                command = 'source %s && %s' % (self.download_command_prefix, command)
            print '#' * 100
            print 'Start to download %s build from sona' % (self.project_name)
            local(command)
            print '#' * 100
    
    # 解压zip文件，并返回解压后的项目目录
    def unzip_build_in_local(self):
        zip_file = self.download_build_file_dir + os.sep + self.downloaded_build_file_name
        local('unzip -o %s -d %s' % (zip_file, self.deploy_dir))
        time.sleep(2)
        project_folder = os.listdir(self.deploy_dir)[0]
        project_deploy_dir = self.deploy_dir + os.sep + project_folder + os.sep
        env.project_deploy_dir = project_deploy_dir
        self.project_deploy_dir = project_deploy_dir
    
    # 合并golden_config_file与change_file， 如果不为None，则赋值merge后的文件到dest_file
    def merge_golden_config_in_local(self):
        golden_config_file = '%s/conf/%s-golden.properties' % (self.project_deploy_dir, self.project_name)
        change_file = self.change_file if hasattr(self, 'change_file') else '%s/%s-changes.properties' % (os.getcwd(), self.project_name)
        merged_config_file = '%s/%s.properties' % (os.getcwd(), self.project_name)
        
        print 'Merge golden config file %s by %s' % (golden_config_file, change_file)
        common_util.merge_properties(golden_config_file, change_file)
        
        print 'Copy %s to %s' % (golden_config_file, merged_config_file)
        local('cp %s %s' % (golden_config_file, merged_config_file))
        self.merged_config_file = merged_config_file
    
    def update_remote_build(self):
        pass
    
    def upload_build_and_do_golden_script(self, dp_golden=True):
        with cd('/tmp'):
            run('rm -rf %s' % (self.downloaded_build_file_name), pty=False)
            run('rm -rf %s' % (self.deploy_dir), pty=False)
            run('mkdir -p %s' % (self.deploy_dir), pty=False)
        
        with lcd(self.download_build_file_dir):
            put(self.downloaded_build_file_name, '/tmp')
        
        with cd('/tmp'):
            run('unzip -o %s -d %s' % (self.downloaded_build_file_name, self.deploy_dir))
        
        if dp_golden:
            print '#' * 100
            print 'Use golden config to setup environment'
            with cd(env.project_deploy_dir):
                run('chmod a+x setup.sh', pty=False)
                run('./setup.sh', pty=False)
        else:
            print '#' * 100
            print 'Not do golden, just copy war'
            with cd(env.project_deploy_dir):
                run('cp %s*.war %s/%s.war' % (self.project_name, self.tomcat_dir + 'webapps', self.project_name), pty=False)
    
    def update_remote_conf(self):
        pass
    
    # 上传merger后的配置文件和golden.config.file.list到远端.比如logback.xml
    def upload_config_to_remote_tomcat(self):
        print '#' * 100
        print 'Upload configuration file %s onto %s' % (self.merged_config_file, self.tomcat_conf_dir)
        
        # upload configured files to tomcat/lib
        put(self.merged_config_file, self.tomcat_conf_dir)
           
        if self.golden_files:
            for golden_file in self.golden_files.split(','):
                if os.path.exists('%s/%s' % (here, golden_file)):
                    put('%s/%s' % (here, golden_file), self.tomcat_conf_dir)
                else:
                    print 'Golden file %s is not exist in %s, not upload it.' % (golden_file, here)
        
        run('chown -R tomcat:tomcat ' + os.path.dirname(self.tomcat_conf_dir), pty=False)
    
    # 所有的deploy的子类的通用的运行方法。 运行之前需要运行init_component_deploy_parameters方法提前设置好需要的参数
    def run(self, deploy_dir='/tmp/deploy/', **deploy_parameters):
        try:
            self.init_log()
            self.init_configred_parameters()
            self.init_component_deploy_parameters(deploy_dir, **deploy_parameters)
            self.init_deploy_dir()
            self.init_fab_ssh_env()
            self.init_fab_roles(**deploy_parameters)
            self.download_build()
            self.unzip_build_in_local()
            self.update_remote_build()
            self.merge_golden_config_in_local()
            self.update_remote_conf()
        except Exception, e:
            print '#' * 100
            print red('Failed to do deployment. Line:%s, Reason: %s' % (sys.exc_info()[2].tb_lineno, str(e)))
            abort(1)

class DeployCoreVEX(VEXAutoDeployBase, Task):
    here = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self, config_file):
        super(DeployCoreVEX, self).__init__(config_file)
        
    # 非通用，每个是自己的
    def init_fab_roles(self, **kwargs):
        print 'Setup fabric roles (core vex and memcached server)'
        if not self.parameters.has_key('core.vex.server.list'):
            raise Exception('not found core vex server list configuration by "core.vex.server.list"')
        else:
            core_vex_server_list = [self.user + '@' + core_ip for core_ip in self.parameters.get('core.vex.server.list').split(',')]
            fab_util.setRoles('core_vex_server', core_vex_server_list)
        
        if not self.parameters.has_key('memcached.server.list'):
            raise Exception('not found memcached server list configuration by "memcached.server.list"')
        else:
            memcached_server_list = [self.user + '@' + core_ip for core_ip in self.parameters.get('memcached.server.list').split(',')]
            fab_util.setRoles('memcached_server', memcached_server_list)
    
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
        
        print 'update cluster.host to internal IP %s' % (env.host)
        with cd(self.tomcat_conf_dir):
            run("sed '/cluster.host=/s/localhost/%s/g' vex.properties > vex-tmp.properties" % (internal_ip), pty=False)
            run('mv vex-tmp.properties vex.properties')
            run('chown -R tomcat:tomcat ' + self.tomcat_conf_dir, pty=False)

here = os.path.dirname(os.path.abspath(__file__))
config_file = here + os.sep + 'config.properties'
d = DeployCoreVEX(config_file)

deploy_dir = '/tmp/deploy-core-vex'
zip_file_name = 'vex.zip'
d.run(deploy_dir, zip_file_name=zip_file_name)
    
        
