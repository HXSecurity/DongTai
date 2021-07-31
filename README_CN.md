# DongTai-engine
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://huoxianclub.github.io/LingZhi/)
[![DongTai-engine](https://img.shields.io/badge/DongTai--engine-v1.0.0-lightgrey)](https://huoxianclub.github.io/LingZhi/#/doc/tutorial/quickstart)
[![Deploy DongTai Engine To AWS Test](https://github.com/HXSecurity/DongTai-engine/actions/workflows/deploy_engine_to_aws_test.yml/badge.svg)](https://github.com/HXSecurity/DongTai-engine/actions/workflows/deploy_engine_to_aws_test.yml)
[![Deploy DongTai Engine To AWS](https://github.com/HXSecurity/DongTai-engine/actions/workflows/deploy_engine_to_aws.yml/badge.svg)](https://github.com/HXSecurity/DongTai-engine/actions/workflows/deploy_engine_to_aws.yml)

## 项目介绍

DongTai-Engine用于处理DongTai探针采集到的数据，功能如下：
  1. 根据方法池数据和污点跟踪算法分析HTTP/HTTPS/RPC请求中是否存在漏洞
  2. 定期处理漏洞验证请求
  3. 定期更新组件中存在的漏洞
  4. 定期清理过期的日志数据
  5. 定期维护探针检测引擎的状态

## 部署方案

基础服务：MySql、Redis

基础服务配置如下：

| 服务名称 | 地址 | 端口 | 其他配置 |
| --- | --- | --- | --- |
| MySql | 127.0.0.1 | 3306 | 账号：dongtai<br>密码：dongtai-iast<br>库名：dongtai_webapi |
| Redis | 127.0.0.1 | 6379 | 密码：123456<br>Redis库：0 |

### 官方镜像部署

1. 拉取官方镜像
```shell script
$ docker pull registry.cn-beijing.aliyuncs.com/secnium/iast-saas-engine:1.0.0
```

2. 创建配置文件：`/etc/dongtai/config.ini`，内容如下：
```ini
[mysql]
host = 127.0.0.1
port = 3306
name = dongtai_webapi
user = dongtai
password = dongtai-iast

[redis]
host = 127.0.0.1
port = 6379
password = 123456
db = 0

; 下面的内容未使用，保持默认
[engine]
url = http://engine_url

[apiserver]
url = http://api_server_url

[smtp]
server = server
user = user
password = password
from_addr = from_addr
ssl = False
cc_addr = cc_addr

[aliyun_oss]
access_key = access_key
access_key_secret = access_key
```

3. 启动`dongtai-engine`容器并映射配置文件
```shell script
$ docker run -d --name dongtai-engine -v /etc/dongtai/config.ini:/opt/dongtai/engine/conf/config.ini --restart=always secnium/iast-saas-engine:1.0.0
```

4. 启动`dongtai-engine-task`容器并映射配置文件
```shell script
$ docker run -d --name dongtai-engine-task -v /etc/dongtai/config.ini:/opt/dongtai/engine/conf/config.ini --restart=always secnium/iast-saas-engine:1.0.0 bash /opt/dongtai/engine/docker/entrypoint.sh
```

### 构建镜像部署

1. 构建镜像
```shell script
$ docker build -t secnium/iast-saas-engine:1.0.0 .
```

2. 创建配置文件：`/etc/dongtai/config.ini`，内容如下：
```ini
[mysql]
host = 127.0.0.1
port = 3306
name = dongtai_webapi
user = dongtai
password = dongtai-iast

[redis]
host = 127.0.0.1
port = 6379
password = 123456
db = 0

; 下面的内容未使用，保持默认
[engine]
url = http://engine_url

[apiserver]
url = http://api_server_url

[smtp]
server = server
user = user
password = password
from_addr = from_addr
ssl = False
cc_addr = cc_addr

[aliyun_oss]
access_key = access_key
access_key_secret = access_key
```

3. 启动`dongtai-engine`容器并映射配置文件
```shell script
$ docker run -d --name dongtai-engine -v /etc/dongtai/config.ini:/opt/dongtai/engine/conf/config.ini --restart=always secnium/iast-saas-engine:1.0.0
```

4. 启动`dongtai-engine-task`容器并映射配置文件
```shell script
$ docker run -d --name dongtai-engine-task -v /etc/dongtai/config.ini:/opt/dongtai/engine/conf/config.ini --restart=always secnium/iast-saas-engine:1.0.0 bash /opt/dongtai/engine/docker/entrypoint.sh
```

### 文档
- [官方文档](https://hxsecurity.github.io/DongTai-Doc/#/)
- [洞态官网](https://iast.huoxian.cn/)
