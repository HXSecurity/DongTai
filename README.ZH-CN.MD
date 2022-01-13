# DongTai-openapi

[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://https://github.com/HXSecurity/DongTai)
[![DongTai-openapi](https://img.shields.io/github/v/release/HXSecurity/Dongtai-openapi?label=Dongtai-openapi)](https://github.com/HXSecurity/DongTai-openapi/releases)

[![Deploy DongTai OpenAPI To AWS Test](https://github.com/HXSecurity/DongTai-openapi/actions/workflows/deploy_openapi_to_aws_test.yml/badge.svg)](https://github.com/HXSecurity/DongTai-openapi/actions/workflows/deploy_openapi_to_aws_test.yml)
[![Deploy DongTai OpenAPI To AWS](https://github.com/HXSecurity/DongTai-openapi/actions/workflows/deploy_openapi_to_aws.yml/badge.svg)](https://github.com/HXSecurity/DongTai-openapi/actions/workflows/deploy_openapi_to_aws.yml)
[![Release DongTai OpenAPI](https://github.com/HXSecurity/DongTai-openapi/actions/workflows/release_openapi.yml/badge.svg)](https://github.com/HXSecurity/DongTai-openapi/actions/workflows/release_openapi.yml)

[English](README.MD)

## 项目介绍
DongTai-OpenAPI用于处理DongTai探针的相关请求，包括：
- 处理agent注册请求
- 处理心跳数据
- 处理错误日志数据
- 处理第三方组件数据
- 处理方法调用数据
- 处理权限注册/变更等数据
- 发送探针控制指令
- 发送hook策略
- 下载检测引擎等

## 部署方案
基础服务：MySql、DongTai-Engine

基础服务配置如下：

| 服务名称 | 地址 | 端口 | 其他配置 |
| --- | --- | --- | --- |
| MySql | 127.0.0.1 | 3306 | 账号：dongtai<br>密码：dongtai-iast<br>库名：dongtai_webapi |
| DongTai-Engine | 127.0.0.1 | 8081 |  |

### 官方镜像部署

1. 拉取官方镜像
```shell script
$ docker pull registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-openapi:latest
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
host = redis
port = port
password = password
db = 0


[engine]
url = http://127.0.0.1:8081

; 下面的内容未使用，保持默认
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

3. 启动`dongtai-openapi`容器并映射配置文件
```shell script
$ docker run -d --name dongtai-openapi -p 8000:8000 -v /etc/dongtai/config.ini:/opt/dongtai/openapi/conf/config.ini --restart=always huoxian_pub/dongtai-openapi:latest
```

### 构建镜像部署

1. 构建镜像
```shell script
$ docker build -t huoxian_pub/dongtai-openapi:latest .
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
host = redis
port = port
password = password
db = 0


[engine]
url = http://127.0.0.1:8081

; 下面的内容未使用，保持默认
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

3. 启动`dongtai-openapi`容器并映射配置文件
```shell script
$ docker run -d --name dongtai-openapi -p 8000:8000 -v /etc/dongtai/config.ini:/opt/dongtai/openapi/conf/config.ini --restart=always huoxian_pub/dongtai-openapi:latest
```


### 文档
- [官方文档](https://huoxianclub.github.io/LingZhi/#/)
- [快速体验](https://iast.io)
