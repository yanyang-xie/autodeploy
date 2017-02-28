from time import sleep

from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import run
from fabric.state import env
from fabric.tasks import execute

# if you want to run the script using nohup, please run it as "nohup python switch_redis_master_slave.py </dev/null &" 

#redis_hosts = ['54.254.180.197', '54.255.173.250']
redis_hosts = ['172.31.11.105', '172.31.8.135'] #YY_Benchmark redis 5 and 10
user='root'
port=22
public_key_file='/root/ttbj-keypair.pem'
#public_key_file='/Users/xieyanyang/work/ttbj/ttbj-keypair.pem'

redis_start_cmd = 'systemctl start redis.service'
redis_stop_cmd = 'systemctl stop redis.service'

@task
def stop_redis(redis_host, is_kill=True):
    with settings(host_string=redis_host):
        if is_kill is True:
            print 'Kill redis server in [%s]' %(redis_host)
            kill_redis_service()
        else:
            print 'Stop redis server in [%s]' %(redis_host)
            run(redis_stop_cmd)

@task
def start_redis(redis_host):
    with settings(host_string=redis_host):
        print 'Start redis server in [%s]' %(redis_host)
        run(redis_start_cmd)

def kill_redis_service(service_tag='redis-server'):
    pid = run("ps gaux | grep %s | grep -v grep | awk '{print $2}'" % (service_tag), pty=False, warn_only=True)
    if pid == '':
        return

    pids = str(pid).splitlines()
    if pids is None or len(pids) == 0:
        print 'Service \'%s\' is not running till now.' % (service_tag)
    else:
        print 'Service \'%s\' is running, execute kill.' % (service_tag)
        for p_id in pids:
            try:
                run('kill -9 %s' % (p_id), pty=False, warn_only=True, quiet=True)
            except:
                pass

if __name__ == '__main__':
    if len(redis_hosts) != 2:
        print 'Redis host must be one pair of master and slave'
        exit(1)
    
    env.user=user
    env.key_filename=public_key_file
    env.port=port
    is_kill=True
    
    start_stop_interval = 300
    
    counter = 0
    while(True):
        redis_host_1, redis_host_2 = redis_hosts
        execute(stop_redis, redis_host_1, is_kill)
        sleep(start_stop_interval)
        execute(start_redis, redis_host_1)
        sleep(start_stop_interval)
        
        execute(stop_redis, redis_host_2, is_kill)
        sleep(start_stop_interval)
        execute(start_redis, redis_host_2)
        sleep(start_stop_interval)
        
        if counter > 60 * 60 * 24 * 3:
            break
    print 'Task to switch redis is done.'
