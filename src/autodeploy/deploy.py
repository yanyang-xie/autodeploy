# -*- coding=utf-8 -*-
# author: yanyang.xie@gmail.com

import os
import string
import sys
import time

from fabric.colors import red, blue
from fabric.context_managers import cd, lcd
from fabric.operations import local, put, run
from fabric.utils import abort

# Add project base dir into python sys.path
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], "../.."))
from utility import common_util, log_util, fab_util, download_sona_build, encrypt_util

class AutoDeployBase(object):
    '''
    Basic module for auto deployment
    '''
    def __init__(self, config_file, log_file='/tmp/deloy.log'):
        '''Initialized auto deployment with a properties file and log file'''
        self.config_file = config_file
        self.log_file = log_file
        
        if not os.path.exists(self.config_file):
            print 'Config file %s do not exist' % (self.config_file)
            sys.exit(1)
        self.parameters = common_util.load_properties(self.config_file)
    
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
    '''
    VEX auto deployment script contains following majority steps:
    1. Download build from SONA
    2. Upload build to remote server and then do golden setup or just copy required files
    3. Merge golden-config file with local changes file and then update the configuration file in remote server
    
    In these steps, download build from sona and merge configuration is common.
    What you should do to deploy vex component is just to setup your fabric hosts and other special steps. 
    '''
    def __init__(self, config_file_name='config.properties', config_sub_folder='', log_file='/tmp/deloy.log'):
        '''
        @param config_file_name: default is config.properties
        @param config_sub_folder: If your configuration file is in sub folder from current folder, please fill in it.
        '''
        config_file_name = common_util.get_script_current_dir() + os.sep + config_sub_folder + os.sep + config_file_name
        super(VEXAutoDeployBase, self).__init__(config_file_name, log_file)
        
        self.config_sub_folder = config_sub_folder
        self.tomcat_dir = '/usr/local/thistech/tomcat/'
        self.tomcat_conf_dir = self.tomcat_dir + 'lib/'
        
        self.auto_download_build, self.run_golden_setup_script = (True, True)
        self.user, self.public_key, self.password, self.port, self.golden_files = (None, None, None, None, None)
        self.sona_user_name, self.sona_user_password = (None, None)
        self.project_name, self.project_version, self.project_extension_name = (None, None, None)
        self.download_build_file_dir, self.downloaded_build_file_name, self.download_command_prefix = (None, None, None)
        self.http_proxy, self.https_proxy = (None, None)
    
    def init_configred_parameters(self):
        '''Read configred parameters and then set it as object properties'''
        print '#' * 100
        print 'Initial deplpy parameters from config file %s' % (self.config_file)
        set_attr = lambda attr_name, config_name, default_value = None: self._set_attr(attr_name, common_util.get_config_value_by_key(self.parameters, config_name, default_value))
        
        set_attr('user', 'user', 'root')
        set_attr('port', 'port', '22')
        set_attr('public_key', 'public.key')
        set_attr('password', 'password')
        set_attr('golden_files', 'golden.config.file.list')
        
        auto_download_build = common_util.get_config_value_by_key(self.parameters, 'auto.download.sona.build')
        setattr(self, 'auto_download_build', True if auto_download_build and string.lower(auto_download_build) == 'true' else False)
        print 'auto_download_build:%s' % (self.auto_download_build)
        
        run_golden_setup_script = common_util.get_config_value_by_key(self.parameters, 'run.golden.setup.script')
        setattr(self, 'run_golden_setup_script', True if run_golden_setup_script and string.lower(run_golden_setup_script) == 'true' else False)
        print 'run_golden_setup_script:%s' % (self.run_golden_setup_script)
        
        set_attr('sona_user_name', 'sona.user.name')
        set_attr('sona_user_password', 'sona.user.passwd')
        set_attr('project_name', 'project.name')
        set_attr('project_version', 'project.version')
        set_attr('project_extension_name', 'project.extension.name')
        set_attr('project_version', 'project.version')
        
        set_attr('changes_file_name', 'changes.file.name')
        set_attr('project_config_golden_file_name', 'project.config.golden.file.name')
        set_attr('project_config_default_file_name', 'project.config.default.file.name')
        
        set_attr('download_build_file_dir', 'build.local.file.dir', common_util.get_script_current_dir())
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
            
            setattr(self, 'sona_user_password', encrypt_util.decrypt('Thistech', self.sona_user_password))
        else:
            if getattr(self, 'downloaded_build_file_name') is None:
                raise Exception('Configuration for %s is not set, please check.' % ('build.local.file.name'))
    
    def init_component_deploy_parameters(self, deploy_dir, **kwargs):
        '''Setup deployment directory and other parameters.'''
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
    
    def init_fab_ssh_env(self):
        '''Setup fabric SSH environments'''
        print 'Setup fabric ssh environment'
        if self.public_key is None and self.password is None:
            raise Exception('public.key or password must have one')
        
        if self.public_key:
            fab_util.setKeyFile(getattr(self, 'public_key'))
        
        if self.password:
            fab_util.set_password(getattr(self, 'password'))
        
        if self.user:
            fab_util.set_user(getattr(self, 'user'))
    
    def init_fab_roles(self, **kwargs):
        '''Setup fabric roles, you must implement it in your class'''
        pass
    
    def download_build(self):
        '''Download build from SONA'''
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
    
    def unzip_build_in_local(self):
        '''Unzip build to deployment folder'''
        zip_file = self.download_build_file_dir + os.sep + self.downloaded_build_file_name
        local('unzip -o %s -d %s' % (zip_file, self.deploy_dir), capture=True)
        time.sleep(2)
        project_folder = os.listdir(self.deploy_dir)[0]
        project_deploy_dir = self.deploy_dir + os.sep + project_folder + os.sep
        self.project_deploy_dir = project_deploy_dir
    
    def merge_golden_config_in_local(self):
        '''Replace values in golden_config_file by change_file, then copy merged file into current folder'''
        golden_config_file = '%s/conf/%s' % (self.project_deploy_dir, self.project_config_golden_file_name)
        change_file = self.change_file if hasattr(self, 'change_file') else '%s/%s/%s' % (common_util.get_script_current_dir(), self.config_sub_folder, self.changes_file_name)
        merged_config_file = '%s/%s' % (common_util.get_script_current_dir(), self.project_config_default_file_name)
        
        print 'Merge golden config file %s by %s' % (golden_config_file, change_file)
        common_util.merge_properties(golden_config_file, change_file)
        
        print 'Copy %s to %s' % (golden_config_file, merged_config_file)
        local('cp %s %s' % (golden_config_file, merged_config_file))
        self.merged_config_file = merged_config_file
    
    def update_remote_build(self):
        '''Update remote build, your should run the method with settings(roles=['',],)'''
        pass
    
    def upload_build_and_do_golden_script(self, run_golden_setup_script=True):
        '''Upload build to remote server, and then do golden setup.'''
        with cd('/tmp'):
            run('rm -rf %s' % (self.downloaded_build_file_name), pty=False)
            run('rm -rf %s' % (self.deploy_dir), pty=False)
            run('mkdir -p %s' % (self.deploy_dir), pty=False)
        
        with lcd(self.download_build_file_dir):
            put(self.downloaded_build_file_name, '/tmp')
        
        with cd('/tmp'):
            run('unzip -o %s -d %s' % (self.downloaded_build_file_name, self.deploy_dir))
        
        if run_golden_setup_script:
            print '#' * 100
            print 'Use golden config to setup environment'
            with cd(self.project_deploy_dir):
                run('chmod a+x setup.sh', pty=False)
                run('./setup.sh', pty=False)
        else:
            print '#' * 100
            print 'Not do golden, just copy and rename war'
            with cd(self.project_deploy_dir):
                run('cp %s*.war %s/%s.war' % (self.project_name, self.tomcat_dir + 'webapps', self.project_war_name), pty=False)
    
    def update_remote_conf(self):
        '''Update remote conf, your should run the method with settings(roles=['',],)'''
        pass
    
    def upload_config_to_remote_tomcat(self):
        '''Upload configuration file and required files on to remote tomcat server'''
        print '#' * 100
        print 'Upload configuration file %s onto %s' % (self.merged_config_file, self.tomcat_conf_dir)
        
        # upload configured files to tomcat/lib
        put(self.merged_config_file, self.tomcat_conf_dir)
           
        if self.golden_files:
            for golden_file in self.golden_files.split(','):
                if os.path.exists('%s/%s' % (common_util.get_script_current_dir(), golden_file)):
                    put('%s/%s/%s' % (common_util.get_script_current_dir(), self.config_sub_folder, golden_file), self.tomcat_conf_dir)
                else:
                    print 'Golden file %s is not exist in %s, not upload it.' % (golden_file, common_util.get_script_current_dir())
        
        run('chown -R tomcat:tomcat ' + os.path.dirname(self.tomcat_conf_dir), pty=False)
    
    def set_roles(self, role_name, server_config_name):
        '''Setup fabric roles'''
        server_list = ['%s@%s:%s' % (self.user, core_ip, self.port) for core_ip in self.parameters.get(server_config_name).split(',')]
        fab_util.setRoles(role_name, server_list)
    
    def get_internal_ip(self):
        '''Get internal server ip in remote server'''
        get_internal_ip_shell = '/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk "{print $2}" |tr -d "addr:"'
        output = run(get_internal_ip_shell, pty=False)
        
        internal_ip_list = []
        for line in output.split('\n'):
            if line.strip() == '':
                continue
            internal_ip = line.split('Bcst')[0].replace('inet', '').strip()
            if internal_ip != '':
                internal_ip_list.append(internal_ip)
        
        return internal_ip_list[-1]
    
    def run(self, deploy_dir='/tmp/deploy/', **deploy_parameters):
        '''
        Deployment main method. If need initial deployment parameters, please add it into deploy_parameters
        '''
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
            
            print blue('Finish deploy %s-%s' % (self.project_name, self.project_version))
        except Exception, e:
            print '#' * 100
            print red('Failed to do deployment. Line:%s, Reason: %s' % (sys.exc_info()[2].tb_lineno, str(e)))
            abort(1)