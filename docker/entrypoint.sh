#!/usr/bin/env sh

######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : entrypoint
# @created     : 星期四 1月 20, 2022 15:07:37 CST
#
# @description : 
######################################################################


#MYSQL_HOST=`awk '/\[mysql\]/{flag=1;next}/\[.*\]/{flag=0}flag && NF' /opt/dongtai/webapi/conf/config.ini  | awk -F "=" '/^host/ {print $2}'`
#MYSQL_NAME=`awk '/\[mysql\]/{flag=1;next}/\[.*\]/{flag=0}flag && NF' /opt/dongtai/webapi/conf/config.ini  | awk -F "=" '/^name/ {print $2}'`
#MYSQL_USER=`awk '/\[mysql\]/{flag=1;next}/\[.*\]/{flag=0}flag && NF' /opt/dongtai/webapi/conf/config.ini  | awk -F "=" '/^user/ {print $2}'`
#MYSQL_PASSWORD=`awk '/\[mysql\]/{flag=1;next}/\[.*\]/{flag=0}flag && NF' /opt/dongtai/webapi/conf/config.ini  | awk -F "=" '/^password/ {print $2}'`
#MYSQL_PORT=`awk '/\[mysql\]/{flag=1;next}/\[.*\]/{flag=0}flag && NF' /opt/dongtai/webapi/conf/config.ini  | awk -F "=" '/^port/ {print $2}'`
#
#mysql --host=$MYSQL_HOST -u$MYSQL_USER -P$MYSQL_PORT -p$MYSQL_PASSWORD -D $MYSQL_NAME < /opt/dongtai/webapi/docker/version.sql || true 

python /opt/dongtai/webapi/docker/version_update.py || true

/usr/local/bin/uwsgi --ini /opt/dongtai/webapi/conf/uwsgi.ini
