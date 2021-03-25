#!/bin/bash

echo "start mysqld"
nohup /bin/bash /usr/local/bin/docker-entrypoint.sh mysqld &

echo "sleep until msyqld started"
while :  # 注意加空格
do
    ls /var/run/mysqld/mysqld.sock
    if [ $? -ne 0 ]; then
	    sleep 1
    else
	    break 2
    fi
done

sleep 10

echo "init database"
mysql -uroot -p"dongtai-iast" < /opt/db.sql
mysql -uroot -p"dongtai-iast" < /opt/rule.sql
mysql -uroot -p"dongtai-iast" < /opt/sca.sql

echo "hello" > /tmp/a.log
tail -f /tmp/a.log
