#!/bin/bash
echo '启动uwsgi服务'
python manage.py compilemessages  
sleep 2
python /opt/dongtai/deploy/docker/version_update.py || true
echo $1

if [ "$1" = "worker" ]; then
	celery -A dongtai_conf worker -l info $CONCURRENCY -E --pidfile= 
elif [ "$1" = "worker-beat" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-periodic-task $CONCURRENCY -E --pidfile=
elif [ "$1" = "worker-high-freq" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-method-pool-scan,dongtai-replay-vul-scan $CONCURRENCY -E --pidfile=
elif [ "$1" = "worker-es" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-es-save-task $CONCURRENCY -E --pidfile=  
elif [ "$1" = "worker-sca" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-sca-task $CONCURRENCY -E --pidfile=  
elif [ "$1" = "worker-other" ]; then
	celery -A dongtai_conf worker -l info -X dongtai-periodic-task,dongtai-method-pool-scan,dongtai-replay-vul-scan,dongtai-sca-task $CONCURRENCY -E --pidfile= 
elif [ "$1" = "beat" ]; then
  celery -A dongtai_conf beat -l info $CONCURRENCY  --pidfile= --scheduler django_celery_beat.schedulers:DatabaseScheduler
else
	# /usr/local/bin/uwsgi --ini /opt/dongtai/dongtai_conf/conf/uwsgi.ini --stats :3031 --stats-http
	/usr/local/bin/uwsgi --ini /opt/dongtai/dongtai_conf/conf/uwsgi.ini
fi
