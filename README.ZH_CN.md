# DongTai-webapi
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://https://github.com/HXSecurity/DongTai)
[![DongTai-webapi](https://img.shields.io/github/v/release/HXSecurity/Dongtai-webapi?label=Dongtai-webapi)](https://github.com/HXSecurity/DongTai-webapi/releases)
[![Release DongTai WebApi](https://github.com/HXSecurity/DongTai-webapi/actions/workflows/release_webapi.yml/badge.svg)](https://github.com/HXSecurity/DongTai-webapi/actions/workflows/release_webapi.yml)

[English](README.MD)

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



### 部署方案
- 源码部署
- 容器部署

**源码部署**

1.安装所需的依赖

```
python -m pip install -r requirements-test.txt
```

2.初始化数据库

- 安装MySql 5.7，创建数据库`DongTai-webapi`，运行数据库文件`conf/db.sql`
- 进入`webapi`目录，运行`python manage.py createsuperuser`命令创建管理员

或采用docker部署数据库
- 拉取版本对应的数据库镜像并启动镜像
```
docker pull  registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest 
docker run -itd --name dongtai-mysql -p 3306:3306 registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest 
```


3.修改配置文件

- 复制配置文件`conf/config.ini.example`为`conf/config.ini`并需改其中的配置；其中，`engine`对应的url为`DongTai-engine`的服务地址，`apiserver`对应的url为`DongTai-openapi`的服务地址

4.运行服务

- 运行`python manage.py runserver`启动服务

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


- [官方文档](https://hxsecurity.github.io/DongTai-Doc/#/)
- [快速体验](https://iast.io)
