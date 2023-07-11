#!/bin/bash
echo '启动uwsgi服务'
/bin/bash -c 'mkdir -p /tmp/{logstash/{batchagent,report/{img,word,pdf,excel,html}},iast_cache/package}'
python manage.py compilemessages  
sleep 2
python -c "import deploy.docker.version_update" || true
echo $1

if [ "$1" = "worker" ]; then
	celery -A dongtai_conf worker -l info $DONGTAI_CONCURRENCY -E --pidfile=
elif [ "$1" = "worker-beat" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-periodic-task $DONGTAI_CONCURRENCY -E --pidfile=
elif [ "$1" = "worker-high-freq" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-method-pool-scan,dongtai-replay-vul-scan $DONGTAI_CONCURRENCY -E --pidfile=
elif [ "$1" = "worker-es" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-es-save-task $DONGTAI_CONCURRENCY -E --pidfile=
elif [ "$1" = "worker-sca" ]; then
	celery -A dongtai_conf worker -l info -Q dongtai-sca-task,dongtai-api-route-handler $DONGTAI_CONCURRENCY -E --pidfile=
elif [ "$1" = "worker-other" ]; then
	celery -A dongtai_conf worker -l info -X dongtai-periodic-task,dongtai-method-pool-scan,dongtai-replay-vul-scan,dongtai-sca-task $DONGTAI_CONCURRENCY -E --pidfile=
elif [ "$1" = "beat" ]; then
	celery -A dongtai_conf beat -l info $DONGTAI_CONCURRENCY  --pidfile= --scheduler django_celery_beat.schedulers:DatabaseScheduler
else
	echo "Get the latest vulnerability rules." && python manage.py load_hook_strategy
	if [ $? -ne 0 ]; then echo "ERROR: Lost connection to MySQL server !!!" && exit 1 ; else echo "succeed" ;fi
	uwsgi --ini /opt/dongtai/dongtai_conf/conf/uwsgi.ini $DONGTAI_CONCURRENCY
fi
