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


## 搜索功能发送的数据格式
```json
{
  "name":"cmd-exec-1",
  "msg":"this is a cmd exec",
  "level":"ERROR",
  "sinks":["java.lang.Runtime.exec"],
  "sources":["org.springframework.web.method.support.HandlerMethodArgumentResolverComposite.resolveArgument"]
}
```
id - 规则ID，如果为临时搜索，设置为query，否则，需要设置
msg - 规则对应的信息
security - 规则对应的漏洞ID
sources - source点规则列表
sinks - sink点规则列表
propagators - 传播节点规则列表

目前只支持简单条件

## Sql注入策略
```json
{
  "name":"java-sqli",
  "msg":"Sql注入漏洞策略",
  "level":"high",
  "sinks":["java.sql.Statement.addBatch","java.sql.Statement.execute","java.sql.Statement.executeQuery","java.sql.Connection.prepareCall","java.sql.Connection.prepareStatement",""]
}
```
