echo '启动uwsgi服务'
nohup /usr/local/bin/uwsgi --ini /opt/dongtai/engine/conf/uwsgi.ini &
sleep 2

echo $1

if [ -z $1 ]; then
  echo '启动Celery Worker服务'
  celery -A lingzhi_engine worker -l info -E
else
  echo '启动Celery Beat服务'
  celery -A lingzhi_engine beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
fi
