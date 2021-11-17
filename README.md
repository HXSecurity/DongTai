# DongTai-engine
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://huoxianclub.github.io/DongTai-Doc/)
[![DongTai-engine](https://img.shields.io/badge/DongTai--engine-latest-lightgrey)](https://huoxianclub.github.io/DongTai-Doc/)
[![Deploy DongTai Engine To AWS Test](https://github.com/HXSecurity/DongTai-engine/actions/workflows/deploy_engine_to_aws_test.yml/badge.svg)](https://github.com/HXSecurity/DongTai-engine/actions/workflows/deploy_engine_to_aws_test.yml)
[![Deploy DongTai Engine To AWS](https://github.com/HXSecurity/DongTai-engine/actions/workflows/deploy_engine_to_aws.yml/badge.svg)](https://github.com/HXSecurity/DongTai-engine/actions/workflows/deploy_engine_to_aws.yml)

[中文版本(Chinese version)](README_CN.md)

## Whit is DongTai-Engine?

DongTai-Engine is used to process the data collected by the DongTai probe, and its functions are as follows：
  1. Analyze whether there are vulnerabilities in HTTP/HTTPS/RPC requests based on method pool data and taint tracking algorithms
  2. Handle vulnerability verification requests regularly
  3. Regularly update the vulnerabilities in the components
  4. Regularly clean up expired log data
  5. Regularly maintain the status of the probe detection engine

## Deploy

Basic services：MySql、Redis

The basic service configuration is as follows：

| service name | ip | port | additional |
| --- | --- | --- | --- |
| MySql | 127.0.0.1 | 3306 | account：dongtai<br>password：dongtai-iast<br>database name：dongtai_webapi |
| Redis | 127.0.0.1 | 6379 | password：123456<br>Redis db：0 |

### Official image

1. Pull image
```shell script
$ docker pull registry.cn-beijing.aliyuncs.com/secnium/iast-saas-engine:latest
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
host = 127.0.0.1
port = 6379
password = 123456
db = 0

; The following content unused, keep the default
[engine]
url = http://engine_url


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

3. Start the `dongtai-engine` container and map the configuration file
```shell script
$ docker run -d --name dongtai-engine -v /etc/dongtai/config.ini:/opt/dongtai/engine/conf/config.ini --restart=always secnium/iast-saas-engine:latest
```

4. Start the `dongtai-engine-task` container and map the configuration file
```shell script
$ docker run -d --name dongtai-engine-task -v /etc/dongtai/config.ini:/opt/dongtai/engine/conf/config.ini --restart=always secnium/iast-saas-engine:latest bash /opt/dongtai/engine/docker/entrypoint.sh
```

### Build custom image

1. Build image
```shell script
$ docker build -t secnium/iast-saas-engine:latest .
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
host = 127.0.0.1
port = 6379
password = 123456
db = 0

; The following content unused, keep the default
[engine]
url = http://engine_url

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

3. Start the `dongtai-engine` container and map the configuration file
```shell script
$ docker run -d --name dongtai-engine -v /etc/dongtai/config.ini:/opt/dongtai/engine/conf/config.ini --restart=always secnium/iast-saas-engine:latest
```

4. Start the `dongtai-engine-task` container and map the configuration file
```shell script
$ docker run -d --name dongtai-engine-task -v /etc/dongtai/config.ini:/opt/dongtai/engine/conf/config.ini --restart=always secnium/iast-saas-engine:latest bash /opt/dongtai/engine/docker/entrypoint.sh
```

### Contributing
Contributions are welcomed and greatly appreciated. See [CONTRIBUTING.md](https://github.com/HXSecurity/DongTai/blob/main/CONTRIBUTING.md) for details on submitting patches and the contribution workflow.

Any questions? Let's discuss in [#DongTai discussions](https://github.com/HXSecurity/DongTai/discussions)

### More resources
- [Documentation](https://hxsecurity.github.io/DongTai-Doc/#/)
- [DongTai WebSite](https://iast.huoxian.cn/)

<img src="https://static.scarf.sh/a.png?x-pxid=da98c4b7-4ef2-4e73-a05b-3b3aa43d5f2b" />
