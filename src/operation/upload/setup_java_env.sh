#hosts="172.31.1.52,172.31.1.53,172.31.7.148,172.31.7.149,172.31.8.216,172.31.8.217,172.31.8.218,172.31.8.219"

hosts="172.31.1.52,172.31.1.53,172.31.7.148,172.31.7.149"
hosts="172.31.10.6,172.31.10.8,172.31.10.9,172.31.10.10"
fab -i ~/ttbj-keypair.pem -P -H ${hosts}  -- "cd /usr/local/thistech/conf/ && scp -i ~/ttbj-keypair.pem root@172.31.9.88:/root/thistech/vex-2.0/longevity-instances/operation/environment.properties ."
