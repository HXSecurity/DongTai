# DongTai
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://huoxianclub.github.io/LingZhi/)
[![DongTai--webapi](https://img.shields.io/badge/DongTai--webapi-v1.0.0-lightgrey)](https://github.com/huoxianclub/DongTai-webapi)
[![DongTai--openapi](https://img.shields.io/badge/DongTai--openapi-v1.0.0-lightgrey)](https://github.com/huoxianclub/DongTai-openapi)
[![DongTai--engine](https://img.shields.io/badge/DongTai--engine-v1.0.0-lightgrey)](https://github.com/huoxianclub/DongTai-engine)
[![DongTai--web](https://img.shields.io/badge/DongTai--web-v1.0.0-lightgrey)](https://github.com/huoxianclub/DongTai-web)
[![DongTai--agent--java](https://img.shields.io/badge/DongTai----agent--java-v1.0.0-lightgrey)](https://github.com/huoxianclub/DongTai-agent-java)

## 项目介绍

“火线～洞态IAST”是一款专为甲方安全人员、甲乙代码审计工程师和0 Day漏洞挖掘人员量身打造的辅助工具，可用于集成devops环境进行漏洞检测、作为代码审计的辅助工具和自动化挖掘0 Day。

“火线～洞态IAST”具有五大模块，分别是`DongTai-webapi`、`DongTai-openapi`、`DongTai-engine`、`DongTai-web`、`agent`，其中：
- `DongTai-webapi`用于与`DongTai-web`交互，负责用户相关的API请求；
- `DongTai-openapi`用于与`agent`交互，处理agent上报的数据，向agent下发策略，控制agent的运行等
- `DongTai-engine`用于对`DongTai-openapi`接收到的数据进行分析、处理，计算存在的漏洞和可用的污点调用链等
- `DongTai-web`为“火线～洞态IAST”的前端项目，负责页面展示
- `agent`为各语言的数据采集端，从安装探针的项目中采集相对应的数据，发送至`DongTai-openapi`服务

## 应用场景
“火线～洞态IAST”可应用于：`devsecops`阶段做自动化漏洞检测、开源软件/组件挖掘通用漏洞、上线前安全测试等场景，主要目的是降低现有漏洞检测的工作量，释放安全从业人员的生产力来做更专业的事情。

## 部署

> 一键源码部署Docker环境

Linux/Mac环境，安装docker服务时，可运行`build.sh`脚本，指定当前及机器的内网IP地址，如：192.168.0.1
```
# 拉取最新的代码
$ git clone https://github.com/huoxianclub/DongTai.git DongTai

$ cd DongTai

# 运行shell脚本，一键部署
$ bash build.sh
```
即可成功打包docker镜像并运行，运行之后，通过：http://内网地址 访问即可

> 手动部署

服务之间存在一定的依赖，部署时，需按照顺序进行部署，顺序如下：
- DongTai-webapi
- DongTai-openapi
- DongTai-engine
- DongTai-web
- agent

### DongTai-webapi服务

源码部署

1.初始化数据库

安装MySql 5.7，创建数据库`DongTai-webapi`，运行数据库文件`conf/db.sql`，进入webapi目录，运行`python manage.py createsuperuser`命令创建管理员

2.修改配置文件

复制配置文件`conf/config.ini.example为conf/config.ini`并需改其中的配置，其中:
- engine对应的url为`DongTai-engine`的服务地址
- apiserver对应的url为`DongTai-openapi`的服务地址

3.运行服务

运行`python manage.py runserver`启动服务

### DongTai-openapi服务

1.修改配置文件

复制配置文件`conf/config.ini.example`为`conf/config.ini`并需改其中的配置；其中：

- engine对应的url为`DongTai-engine`的服务地址
- apiserver对应的url为`DongTai-openapi`的服务地址
- 数据库配置为`DongTai-webapi`服务所使用的数据库

2.运行服务

运行`python manage.py runserver`启动服务

### DongTai-engine服务
1.修改配置文件

复制配置文件`conf/config.ini.example`为`conf/config.ini`并需改其中的配置；其中：

- engine对应的url为`DongTai-engine`的服务地址
- apiserver对应的url为`DongTai-openapi`的服务地址
- 数据库配置为`DongTai-webapi`服务所使用的数据库

2.运行服务

运行`python manage.py runserver`启动服务

### DongTai-web服务
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

**DongTai-agent-java**

### 文档
- [官方文档](https://huoxianclub.github.io/LingZhi/#/)
- [快速体验](http://aws.iast.huoxian.cn:8000/login)