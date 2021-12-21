# DongTai-openapi

[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://https://github.com/HXSecurity/DongTai)
[![DongTai-openapi](https://img.shields.io/github/v/release/HXSecurity/Dongtai-openapi?label=Dongtai-openapi)](https://github.com/HXSecurity/DongTai-openapi/releases)

[![Release DongTai OpenAPI](https://github.com/HXSecurity/DongTai-openapi/actions/workflows/release_openapi.yml/badge.svg)](https://github.com/HXSecurity/DongTai-openapi/actions/workflows/release_openapi.yml)

[中文版本(Chinese version)](README.ZH-CN.MD)

## Whit is DongTai-Engine?
DongTai-OpenAPI is used to process DongTai probe related requests, including:
- Process agent registration request
- Processing heartbeat data
- Processing error log data
- Processing third-party component data
- Processing method call data
- Processing authority registration/change and other data
- Send probe control commands
- Send hook strategy
- Download detection engine, etc.

## Deploy

Basic services：MySql、DongTai-Engine

The basic service configuration is as follows：

| service name | ip | port | additional |
| --- | --- | --- | --- |
| MySql | 127.0.0.1 | 3306 | account：dongtai<br>password：dongtai-iast<br>database name：dongtai_webapi |
| DongTai-Engine | 127.0.0.1 | 8081 |  |

### Official image

1. Pull image
```shell script
$ docker pull registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-openapi:latest
```

2. Create a configuration file：`/etc/dongtai/config.ini`，The content is as follows：
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

; The following content unused, keep the default
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

3. Start the `dongtai-openapi` container and map the configuration file
```shell script
$ docker run -d --name dongtai-openapi -p 8000:8000 -v /etc/dongtai/config.ini:/opt/dongtai/openapi/conf/config.ini --restart=always huoxian_pub/dongtai-openapi:latest
```

### Build custom image

1. Build image
```shell script
$ docker build -t huoxian_pub/dongtai-openapi:latest .
```

2. Create a configuration file：`/etc/dongtai/config.ini`，The content is as follows：
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

; The following content unused, keep the default
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

3. Start the `dongtai-openapi` container and map the configuration file
```shell script
$ docker run -d --name dongtai-openapi -p 8000:8000 -v /etc/dongtai/config.ini:/opt/dongtai/openapi/conf/config.ini --restart=always huoxian_pub/dongtai-openapi:latest
```

### Contributing
Contributions are welcomed and greatly appreciated. See [CONTRIBUTING.md](https://github.com/HXSecurity/DongTai/blob/main/CONTRIBUTING.md) for details on submitting patches and the contribution workflow.

Any questions? Let's discuss in [#DongTai discussions](https://github.com/HXSecurity/DongTai/discussions)

### More resources
- [Documentation](https://hxsecurity.github.io/DongTai-Doc/#/)
- [DongTai WebSite](https://iast.io)

<img src="https://static.scarf.sh/a.png?x-pxid=693e2057-a509-4ebc-8322-e084ab861861" />
