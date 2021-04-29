echo '启动uwsgi服务'
nohup /usr/local/bin/uwsgi --ini /opt/iast/engine/conf/uwsgi.ini &
sleep 2
echo '启动celery服务'
nohup celery -A lingzhi_engine worker -l info -E &
sleep 5
celery -A lingzhi_engine beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler