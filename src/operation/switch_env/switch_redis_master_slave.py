from time import sleep

from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import run
from fabric.state import env
from fabric.tasks import execute


redis_hosts = ['54.254.180.197', '54.255.173.250']
#redis_hosts = ['172.31.11.105', '172.31.8.135'] #YY_Benchmark redis 5 and 10
user='root'
port=22
#public_key_file='/root/ttbj-keypair.pem'
public_key_file='/Users/xieyanyang/work/ttbj/ttbj-keypair.pem'

redis_start_cmd = 'systemctl start redis.service'
redis_stop_cmd = 'systemctl stop redis.service'

@task
def stop_redis(redis_host):
    with settings(host_string=redis_host):
        print 'Stop redis server in [%s]' %(redis_host)
        run(redis_stop_cmd)

@task
def start_redis(redis_host):
    with settings(host_string=redis_host):
        print 'Start redis server in [%s]' %(redis_host)
        run(redis_start_cmd)

if __name__ == '__main__':
    if len(redis_hosts) != 2:
        print 'Redis host must be one pair of master and slave'
        exit(1)
    
    env.user=user
    env.key_filename=public_key_file
    env.port=port
    
    start_stop_interval = 30
    
    counter = 0
    while(True):
        redis_host_1, redis_host_2 = redis_hosts
        execute(stop_redis, redis_host_1)
        sleep(start_stop_interval)
        execute(start_redis, redis_host_1)
        sleep(start_stop_interval)
        
        execute(stop_redis, redis_host_2)
        sleep(start_stop_interval)
        execute(start_redis, redis_host_2)
        sleep(start_stop_interval)
        
        if counter > 60 * 60 * 24 * 3:
            break
    print 'Task to switch redis is done.'