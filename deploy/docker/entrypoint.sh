#!/bin/bash
echo '启动uwsgi服务'
python manage.py compilemessages  
sleep 2
python /opt/dongtai/webapi/deploy/docker/version_update.py || true
echo $1

if [ "$1" = "worker" ]; then
	nohup /usr/local/bin/uwsgi --ini /opt/dongtai/webapi/dongtai_conf/conf/uwsgi.ini &
	celery -A dongtai_conf worker -l info -E --pidfile=
elif [ "$1" = "beat" ]; then
	nohup /usr/local/bin/uwsgi --ini /opt/dongtai/webapi/dongtai_conf/conf/uwsgi.ini  &
  celery -A dongtai_conf beat -l info --pidfile= --scheduler django_celery_beat.schedulers:DatabaseScheduler
else
	# /usr/local/bin/uwsgi --ini /opt/dongtai/webapi/conf/uwsgi.ini --stats :3031 --stats-http
	/usr/local/bin/uwsgi --ini /opt/dongtai/webapi/dongtai_conf/conf/uwsgi.ini
fi
