# DongTai-webapi
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://github.com/HXSecurity/DongTai)
[![DongTai-webapi](https://img.shields.io/github/v/release/HXSecurity/Dongtai-webapi?label=Dongtai-webapi)](https://github.com/HXSecurity/DongTai-webapi/releases)
[![Release DongTai WebApi](https://github.com/HXSecurity/DongTai-webapi/actions/workflows/release_webapi.yml/badge.svg)](https://github.com/HXSecurity/DongTai-webapi/actions/workflows/release_webapi.yml)

[English](README.md)

## 项目介绍
DongTai-WebAPI 用于处理DongTai用户资源管理的相关请求，包括：


- 项目管理请求
- 漏洞管理
- 用户数据检索
- 系统配置资源
- 用户/角色管理
- Agent部署管理
- 租户管理
- 部署文档检索

## 如何贡献代码

### 开发

- 使用docker-compose (推荐)
- 使用batect(试验阶段，在官方移除jdk依赖后转为推荐)
- 不使用docker-compose

提示：避免使用前两种之外的方式，这不仅能减少配置本地开发环境的时间，同时也能够减少开发环境与分发环境相异导致的测试错误、兼容性错误等等问题。

#### 使用docker-compose (推荐)

1. 初始化环境
```
cp config.ini.example config.ini
```

2. 使用docker-compose启动项目

```
docker-compose -p dongtai-iast-dev up -d
```
该命令会构建当前目录下的webapi镜像,并拉取洞态IAST中最少的所需镜像。其中除了基于当前目录构建的`dongtai-webapi`以外，还包括`dongtai-openapi`、`dongtai-web`、`dongtai-mysql`、`dongtai-redis`这几个镜像。
如果需要完整的服务，使用以下命令

```
docker-compose -p dongtai-iast-dev up -d --scale dongtai-engine=1  --scale dongtai-engine-task=1
```

其中的`dongtai-mysql`暴露了33060端口以方便开发者从外部链接mysql，而`dongtai-webapi`会额外暴露8010端口，方便开发者使用除uwsgi启动外的方式调试，如`python manage.py runserver 0.0.0.0:8010`。

3. 当修改代码后
使用一下命令重启webapi服务，服务将会以修改后的代码启动
```
docker-compose -p dongtai-iast-dev restart dongtai-webapi
```

如果修改了部署相关的内容，请使用一下命令重新build镜像
```
docker-compose -p dongtai-iast-dev up -d --build
```

4. 额外

如果你希望使用在开发过程中使用[python-agent](https://github.com/HXSecurity/DongTai-agent-python)进行安全检测，这已经在docker-compose与代码里预留了设置。

a.在[洞态IAST-帐号注册](https://jinshuju.net/f/I9PNmf?from=webapi)申请帐号

b.下载所属的dongtai-python-agent.tar.gz并放置在webapi的当前目录下

c.执行以下命令并取消docker-compose.yml中`- PYTHONAGENT=TRUE`

```
docker exec -it dongtai-iast-dev_dongtai-webapi_1 pip install dongtai-agent-python.tar.gz
```

d.使用3.中的命令重启服务

#### 使用batect

1. 运行`./batect` 检测依赖是否满足，以及初始化batect。

2. 运行`./batect --list-tasks` 查看现有的task，如下：

```
integration:
- integration-test-all: integration with all components
- integration-test-web: integration with web front-end

serve:
- serve: Serve the webapi application standingalone
- serve-with-db: Serve the webapi application with db

test:
- test: run webapi unittest
```

例如：
运行以下命令，将构建单独的webapi容器和db容器。
```
./batect serve-with-db
```
其中可使用如下环境变量。

- DOC: ${WEBAPI_DOC:-TRUE}
- debug: ${WEBAPI_debug:-true}
- SAVEEYE: ${WEBAPI_SAVEEYE:-TRUE}
- REQUESTLOG: ${WEBAPI_REQUESTLOG:-TRUE}
- CPROFILE: ${WEBAPI_CPROFILE:-TRUE}
- PYTHONAGENT: ${WEBAPI_PYTHON_AGENT:-FALSE}
- PROJECT_NAME: ${WEBAPI_PROJECT_NAME:-LocalWEBAPI}
- PROJECT_VERSION: ${WEBAPI_PROJECT_VERSION:-v1.0}
- LOG_PATH: ${WEBAPI_LOG_PATH:-/tmp/dongtai-agent-python.log}
- DONGTAI_IAST_BASE_URL: ${DONGTAI_IAST_BASE_URL:-https://iast.io/openapi}
- DONGTAI_AGNET_TOKEN: ${DONGTAI_AGNET_TOKEN:-79798299b48839c84886d728958a8f708e119868}

例：
使用主机环境变量覆盖默认值，启用PYTHONAGENT:
```
WEBAPI_PYTHON_AGENT=TRUE ./batect serve-with-db
```

[Batect安装](https://batect.dev/docs/getting-started/installation)
[Batect入门](https://batect.dev/docs/getting-started/tutorial)


#### 使用本地环境

1.安装所需的依赖

```
python -m pip install -r requirements-test.txt
```

注释:windows下无法安装jq，jq用于处理敏感信息的json解析，若非开发相关功能可忽略，或是在windows下采用WSL进行开发


2.初始化数据库


- 拉取版本对应的数据库镜像并启动镜像
```
docker pull  dongtai/dongtai-mysql:latest 
docker run -itd --name dongtai-mysql -p 3306:3306 dongtai/dongtai-mysql:latest
```

若需要创建或修改数据库表，请参照[DongTai-Base-Image](https://github.com/HXSecurity/Dongtai-Base-Image)仓库规范，并提交相关更改的.sql文件


3.修改配置文件

- 复制配置文件`conf/config.ini.example`为`conf/config.ini`并需改其中的配置；其中，`engine`对应的url为`DongTai-engine`的服务地址，`apiserver`对应的url为`DongTai-openapi`的服务地址
- 只开发webapi相关的功能时可以不填engine和apiserver

4.运行服务调试

开发相关的环境变量
PYTHONAGENT=TRUE 开启pythonagent，需要手动安装，参照[PythonAgent安装](http://doc.dongtai.io/02_start/03_agent.html#python-agent)
DOC=TRUE 开启swagger 路径为 `/api/XZPcGFKoxYXScwGjQtJx8u/schema/swagger-ui/`
debug=true 开启debug模式

- 运行`python manage.py runserver`启动服务

### 文档

- 项目内置的API文档

1. 启动容器时加上文档相关的参数:
```
$ docker run -d -p 8000:8000 --restart=always -e environment=DOC --name dongtai-webapi huoxian/dongtai-webapi:latest
```
此处需要启动对应的mysql数据库，如果仅希望单独启动webapi项目查看文档，则需额外加上以下参数 `-e database=sqlite`（仅为单独启动webapi项目查看文档，不保证在sqlite下的兼容性),完整命令为:
```
$ docker run -d -p 8000:8000 --restart=always -e environment=DOC -e database=sqlite --name dongtai-webapi huoxian/dongtai-webapi:latest
```

2. 访问容器中对应的API:

Swagger-ui地址为 `http://<containerip:port>/api/XZPcGFKoxYXScwGjQtJx8u/schema/swagger-ui/#/`

Redoc地址为 `http://<containerip:port>/api/XZPcGFKoxYXScwGjQtJx8u/schema/redoc/`

若需要单独需要导出swagger.json
地址为 `http://<containerip:port>/api/XZPcGFKoxYXScwGjQtJx8u/schema/`

3. 具体的API鉴权模式已包含在API文档中，可在web的安装agent界面找到对应的token。

## 部署

### 部署方案

- 使用[DongTai](https://github.com/HXSecurity/DongTai) 中提供的工具进行(推荐)
- 源码部署
- 容器部署


**容器部署** 

1.初始化数据库

- 拉取版本对应的数据库镜像
```
docker pull  registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest 
docker run -itd --name dongtai-mysql -p 3306:3306 registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest 
```


2.修改配置文件

复制配置文件`conf/config.ini.example`为`conf/config.ini`并需改其中的配置；其中：
- `engine`对应的url为`DongTai-engine`的服务地址
- `apiserver`对应的url为`DongTai-openapi`的服务地址

3.构建镜像
```
$ docker build -t huoxian/dongtai-webapi:latest .
```

4.启动容器
```
$ docker run -d -p 8000:8000 --restart=always --name dongtai-webapi huoxian/dongtai-webapi:latest
```


**源码部署**

1.安装所需的依赖

```
python -m pip install -r requirements-prod.txt
```

2.初始化数据库

- 安装MySql 5.7，创建数据库`DongTai-webapi`，运行数据库文件`conf/db.sql`
- 进入`webapi`目录，运行`python manage.py createsuperuser`命令创建管理员

或采用docker部署数据库
- 拉取版本对应的数据库镜像并启动镜像
```
docker pull  dongtai/dongtai-mysql:latest 
docker run -itd --name dongtai-mysql -p 3306:3306 dongtai/dongtai-mysql:latest
```


3.修改配置文件

- 复制配置文件`conf/config.ini.example`为`conf/config.ini`并需改其中的配置；其中，`engine`对应的url为`DongTai-engine`的服务地址，`apiserver`对应的url为`DongTai-openapi`的服务地址

4.运行服务

- 运行`python manage.py runserver`启动服务


- [官方文档](https://doc.dongtai.io/)
- [快速体验](https://iast.io)
