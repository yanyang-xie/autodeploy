# -*- coding=utf-8 -*-
# author: yanyang.xie@thistech.com

import os
import string

from fabric.colors import red
from fabric.contrib.files import exists
from fabric.decorators import roles, task, parallel
from fabric.operations import run
from fabric.tasks import execute
from fabric.state import env
from fabric.context_managers import cd

user = 'root'
pub_key = '/Users/xieyanyang/work/ttbj/ttbj-keypair.pem'
password = ''
port = '22'

vex_server = '54.169.51.190'
nginx_server = '54.169.51.190'

tomcat_dir = '/usr/local/thistech/tomcat'
nginx_conf = '/etc/nginx/nginx.conf'

vex_27_backup_dir = '/root/vex-backup/2.7/vex'
vex_28_backup_dir = '/root/vex-backup/2.8/vex'

nginx_27_backup_dir= '/root/vex-backup/2.7/nginx'
nginx_28_backup_dir= '/root/vex-backup/2.8/nginx'


@task()
def back_up_27():
    execute(back_up_all, vex_27_backup_dir, nginx_27_backup_dir)

@task()
def back_up_28():
    execute(back_up_all, vex_28_backup_dir, nginx_28_backup_dir)

@task()
def revert_from_27():
    execute(revert_all, vex_27_backup_dir, nginx_27_backup_dir)

@task()
def revert_from_28():
    execute(revert_all, vex_28_backup_dir, nginx_28_backup_dir)

@task()
def rm_backup_27():
    execute(rm_back_up, vex_27_backup_dir, nginx_27_backup_dir)

@task()
def rm_backup_28():
    execute(rm_back_up, vex_28_backup_dir, nginx_28_backup_dir)

#----------------------------------------#
@task
@parallel
@roles('vex_server')
def backup_vex_server(backup_dir, vex_server_dir=tomcat_dir, force_backup=False):
    if force_backup is False and exists(backup_dir):
        print 'backup dir %s already exists, not update' %(backup_dir)
        return
    
    print 'backup %s to %s' %(vex_server_dir, backup_dir)
    run('mkdir -p %s' %(backup_dir))
    run('cp -rf %s %s' %(vex_server_dir, backup_dir))
    
            
@task
@parallel
@roles('nginx_server')
def backup_nginx_conf(backup_dir, nginx_conf=nginx_conf, force_backup=False):
    if force_backup is False and exists(backup_dir + os.sep + nginx_conf):
        print 'Nginx backup file %s already exists, not update' %(backup_dir + os.sep + nginx_conf)
        return
    
    print 'backup nginx file from %s to %s' %(nginx_conf, backup_dir)
    run('mkdir -p %s' %(backup_dir))
    run('cp -rf %s %s' %(nginx_conf, backup_dir))

@task()
def back_up_all(tomcat_backup_dir, nginx_backup_dir):
    execute(backup_vex_server, tomcat_backup_dir)
    execute(backup_nginx_conf, nginx_backup_dir)

@task
@parallel
@roles('vex_server')
def rm_backup_vex_server(backup_dir):
    run('rm -rf %s' %(backup_dir))

@task
@parallel
@roles('nginx_server')
def rm_backup_nginx_conf(backup_dir):
    run('rm -rf %s' %(backup_dir))

@task()
def rm_back_up(tomcat_backup_dir, nginx_backup_dir):
    execute(rm_backup_vex_server, tomcat_backup_dir)
    execute(rm_backup_nginx_conf, nginx_backup_dir)

@task
@parallel
@roles('vex_server')
def revert_vex_server(backup_dir, vex_server_dir=tomcat_dir):
    if exists(backup_dir):
        run('cp -rf %s %s' %(backup_dir + os.sep + vex_server_dir.split('/')[-1], string.join(tomcat_dir.split('/')[0:-1], '/')))
    else:
        print red('not found backup server in %s' %(backup_dir))

@task
@parallel
@roles('nginx_server')
def revert_nginx_server(backup_dir, nginx_conf=nginx_conf):
    if exists(backup_dir):
        run('cp -rf %s %s' %(backup_dir + os.sep + nginx_conf.split('/')[-1], nginx_conf))
    else:
        print red('not found backup nginx conf in %s' %(backup_dir))

@task()
@parallel
@roles('vex_server')
def revert_all(tomcat_backup_dir, nginx_backup_dir):
    execute(revert_vex_server, tomcat_backup_dir)
    execute(revert_nginx_server, nginx_backup_dir)

@task()
@parallel
@roles('vex_server')
def change_jdk_to_17():
    with cd('/usr/local/thistech/conf'):
        env_file = 'environment.properties'
        run("sed '/JAVA_HOME=/s/jdk1.8.0_91/jdk1.7.0_60/g' %s > tmp.properties" %(env_file), pty=False)
        run('mv tmp.properties %s' %(env_file))
        run('chown -R tomcat:tomcat ' + env_file, pty=False)

@task()
@parallel
@roles('vex_server')
def change_jdk_to_18():
    with cd('/usr/local/thistech/conf'):
        env_file = 'environment.properties'
        run("sed '/JAVA_HOME=/s/jdk1.7.0_60/jdk1.8.0_91/g' %s > tmp.properties" %(env_file), pty=False)
        run('mv tmp.properties %s' %(env_file))
        run('chown -R tomcat:tomcat ' + env_file, pty=False)

def setRoles(role_name, host_list, user=None, port=None, roledefs_dict=None):
    if host_list is None or type(host_list) != list:
        return
    
    if user:
        host_list = ['%s@%s' % (user, host) for host in host_list if host.find(user) < 0 ]
    
    if port:
        host_list = ['%s:%s' % (host, port)  for host in host_list if host.find(':') < 0 ]
    
    env.roledefs.update({role_name:host_list})
    if roledefs_dict and type(roledefs_dict) is dict:
        env.roledefs.update(roledefs_dict)

def set_hosts(hosts):
    env.hosts += hosts if type(hosts) is list else [hosts, ]

def setKeyFile(key_filename):
    if key_filename is None or key_filename == '':
        return
    env.key_filename = key_filename

def set_user(user):
    if user is None or user == '':
        return
    env.user = user
    
def set_password(password):
    if password is None or password == '':
        return
    env.password = password

def _setup_fab_env():
    # setup fabric parameters
    setKeyFile(pub_key)
    set_password(password)
    
    _setup_facric_roles('vex_server', vex_server, user, port)
    _setup_facric_roles('nginx_server', nginx_server, user, port)

def _setup_facric_roles(role, host_string, user='root', port=22, host_sep=','):
    if role is None:
        return
    
    if host_string is not None and len(host_string) > 0:
        host_list = string.split(host_string, host_sep)
        setRoles(role, host_list, user, port)

_setup_fab_env()