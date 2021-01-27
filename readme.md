# IAST云端检测引擎

## 功能
- 根据hook规则，查找漏洞

## 启动
```shell script
echo '启动uwsgi服务'
nohup /usr/local/bin/uwsgi --ini /opt/iast/engine/conf/uwsgi.ini &
sleep 2
echo '启动celery服务'
celery -A lingzhi_engine worker -l info -E
```