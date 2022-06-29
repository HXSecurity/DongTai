#!/bin/bash
echo '启动uwsgi服务'
python manage.py compilemessages  
sleep 2
python /opt/dongtai/deploy/docker/version_update.py || true
echo $1

if [ "$1" = "worker" ]; then
	celery -A dongtai_conf worker -l info -E --pidfile=
elif [ "$1" = "worker-beat" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-periodic-task -E --pidfile=
elif [ "$1" = "worker-high-freq" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-method-pool-scan,dongtai-replay-vul-scan -E --pidfile=
elif [ "$1" = "worker-other" ]; then
	celery -A dongtai_conf worker -l info -X dongtai-periodic-task,dongtai-method-pool-scan,dongtai-replay-vul-scan -E --pidfile=
elif [ "$1" = "beat" ]; then
  celery -A dongtai_conf beat -l info --pidfile= --scheduler django_celery_beat.schedulers:DatabaseScheduler
else
	# /usr/local/bin/uwsgi --ini /opt/dongtai/dongtai_conf/conf/uwsgi.ini --stats :3031 --stats-http
	/usr/local/bin/uwsgi --ini /opt/dongtai/dongtai_conf/conf/uwsgi.ini
fi
