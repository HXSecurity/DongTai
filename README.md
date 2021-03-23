# dongtai
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![dongtai-project](https://img.shields.io/badge/dongtai%20versions-beta-green)](https://huoxianclub.github.io/LingZhi/)
[![dongtai--webapi](https://img.shields.io/badge/dongtai--webapi-v1.0.0-lightgrey)](https://github.com/huoxianclub/dongtai-webapi)
[![dongtai--openapi](https://img.shields.io/badge/dongtai--openapi-v1.0.0-lightgrey)](https://github.com/huoxianclub/dongtai-openapi)
[![dongtai--engine](https://img.shields.io/badge/dongtai--engine-v1.0.0-lightgrey)](https://github.com/huoxianclub/dongtai-engine)
[![dongtai--web](https://img.shields.io/badge/dongtai--web-v1.0.0-lightgrey)](https://github.com/huoxianclub/dongtai-web)
[![dongtai--agent--java](https://img.shields.io/badge/dongtai----agent--java-v1.0.0-lightgrey)](https://github.com/huoxianclub/dongtai-agent-java)

## 项目介绍

“火线～洞态IAST”是一款专为甲方安全人员、甲乙代码审计工程师和0 Day漏洞挖掘人员量身打造的辅助工具，可用于集成devops环境进行漏洞检测、作为代码审计的辅助工具和自动化挖掘0 Day。

“火线～洞态IAST”具有五大模块，分别是`dongtai-webapi`、`dongtai-openapi`、`dongtai-engine`、`dongtai-web`、`agent`，其中：
- `dongtai-webapi`用于与`dongtai-web`交互，负责用户相关的API请求；
- `dongtai-openapi`用于与`agent`交互，处理agent上报的数据，向agent下发策略，控制agent的运行等
- `dongtai-engine`用于对`dongtai-openapi`接收到的数据进行分析、处理，计算存在的漏洞和可用的污点调用链等
- `dongtai-web`为“火线～洞态IAST”的前端项目，负责页面展示
- `agent`为各语言的数据采集端，从安装探针的项目中采集相对应的数据，发送至`dongtai-openapi`服务

## 应用场景
“火线～洞态IAST”可应用于：`devsecops`阶段做自动化漏洞检测、开源软件/组件挖掘通用漏洞、上线前安全测试等场景，主要目的是降低现有漏洞检测的工作量，释放安全从业人员的生产力来做更专业的事情。

## 部署
服务之间存在一定的依赖，部署时，需按照顺序进行部署，顺序如下：
- dongtai-webapi
- dongtai-openapi
- dongtai-engine
- dongtai-web
- agent

### dongtai-webapi服务

源码部署

1.初始化数据库

安装MySql 5.7，创建数据库`dongtai-webapi`，运行数据库文件`conf/db.sql`，进入webapi目录，运行`python manage.py createsuperuser`命令创建管理员

2.修改配置文件

复制配置文件`conf/config.ini.example为conf/config.ini`并需改其中的配置，其中:
- engine对应的url为`dongtai-engine`的服务地址
- apiserver对应的url为`dongtai-openapi`的服务地址

3.运行服务

运行`python manage.py runserver`启动服务

### dongtai-openapi服务

1.修改配置文件

复制配置文件`conf/config.ini.example`为`conf/config.ini`并需改其中的配置；其中：

- engine对应的url为`dongtai-engine`的服务地址
- apiserver对应的url为`dongtai-openapi`的服务地址
- 数据库配置为`dongtai-webapi`服务所使用的数据库

2.运行服务

运行`python manage.py runserver`启动服务

### dongtai-engine服务
1.修改配置文件

复制配置文件`conf/config.ini.example`为`conf/config.ini`并需改其中的配置；其中：

- engine对应的url为`dongtai-engine`的服务地址
- apiserver对应的url为`dongtai-openapi`的服务地址
- 数据库配置为`dongtai-webapi`服务所使用的数据库

2.运行服务

运行`python manage.py runserver`启动服务

### dongtai-web服务
1.安装`npm`依赖
```bash
$ npm install
```

2.编译为可发布版本
```bash
$ npm run build
```

3.将`dist`目录放入nginx服务的静态资源目录

4.修改nginx配置，设置前端接口对应的后端服务，nginx的配置可参考`nginx.conf`

### agent的部署

**dongtai-agent-java**

### 文档
- [官方文档](https://huoxianclub.github.io/LingZhi/#/)
- [快速体验](http://aws.iast.huoxian.cn:8000/login)