from os.path import sys

from fabric.context_managers import cd
from fabric.contrib.files import exists
from fabric.decorators import task, parallel, roles
from fabric.operations import run
from fabric.state import env
from fabric.tasks import execute


hosts=['172.31.13.47','172.31.13.48','172.31.13.17','172.31.13.18']
user='root'
port=22
public_key_file='/root/ttbj-keypair.pem'
#public_key_file='/Users/xieyanyang/work/ttbj/ttbj-keypair.pem'

tomcat_conf_dir='/usr/local/thistech/tomcat/lib'

@task
@parallel
@roles('vex_service')
def disable_reids():
    #redis.enabled=false
    print 'update redis.enabled to false'
    with cd(tomcat_conf_dir):
        for config_file_name in ['vex.properties', 'vex-frontend.properties']:
            if exists(config_file_name) is True:
                run("sed '/redis.enabled=/s/true/false/g' %s > vex-tmp.properties" % (config_file_name), pty=False)
                run('mv vex-tmp.properties %s' % (config_file_name))
        run('chown -R tomcat:tomcat ' + tomcat_conf_dir, pty=False)
    print 'Finish to disable redis serivce'

@task
@parallel
@roles('vex_service')
def enable_redis():
    #redis.enabled=false
    print 'update redis.enabled to true'
    with cd(tomcat_conf_dir):
        for config_file_name in ['vex.properties', 'vex-frontend.properties']:
            if exists(config_file_name) is True:
                run("sed '/redis.enabled=/s/false/true/g' %s > vex-tmp.properties" % (config_file_name), pty=False)
                run('mv vex-tmp.properties %s' % (config_file_name))
        run('chown -R tomcat:tomcat ' + tomcat_conf_dir, pty=False)
    print 'Finish to enable redis serivce'

# host and role lists will be merge to one list of deduped hosts while execute task
def setRoles(role_name, host_list, user=None, port=None, roledefs_dict=None):
    '''host_list=['root@172.31.13.47:22', 'root@172.31.13.48', ]'''
    if host_list is None or type(host_list) != list:
        return
    
    # env.roledefs = { 'testserver': ['user1@host1:port1',], 'realserver': ['user2@host2:port2', ] }
    if user:
        host_list = ['%s@%s' % (user, host) for host in host_list if host.find(user) < 0 ]
    
    if port:
        host_list = ['%s:%s' % (host, port)  for host in host_list if host.find(':') < 0 ]
    
    env.roledefs.update({role_name:host_list})
    if roledefs_dict and type(roledefs_dict) is dict:
        env.roledefs.update(roledefs_dict)

if __name__ == '__main__':
    setRoles('vex_service', hosts, user, port)
    env.key_filename=public_key_file
    
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'disable':
        execute(disable_reids)
    else:
        execute(enable_redis)
