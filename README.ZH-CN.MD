# DongTai
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![license GPL-3.0](https://img.shields.io/github/license/HXSecurity/DongTai-agent-java)](https://github.com/HXSecurity/DongTai-agent-java/blob/main/LICENSE)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://github.com/HXSecurity/DongTai)
<br>
[![DongTai--webapi](https://img.shields.io/badge/DongTai--webapi-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-webapi)
[![DongTai--openapi](https://img.shields.io/badge/DongTai--openapi-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-openapi)
[![DongTai--engine](https://img.shields.io/badge/DongTai--engine-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-engine)
[![DongTai--web](https://img.shields.io/badge/DongTai--web-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-web)
[![DongTai--agent--java](https://img.shields.io/badge/DongTai----agent--java-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-agent-java)

[English](README.MD)

## DongTai是什么?
DongTai是一款开源的被动式交互式安全测试(IAST)产品，通过动态hook和污点跟踪算法等实现**通用漏洞检测**、**多请求关联漏洞检测(包括但不限于越权漏洞、未授权访问)**、**第三方组件漏洞检测**等，目前支持Java、Python两种语言的应用漏洞检测。

## 技术架构 
"火线-洞态IAST"具有多个基础服务，包括：`DongTai-web`、`DongTai-webapi`、`DongTai-openapi`、`DongTai-engine`、`agent`、`DongTai-deploy`、`DongTai-Base-Image`、`DongTai-Plugin-IDEA`，其中：
- `DongTai-web`是DongTai的产品页面，用于处理用户与洞态的交互
- `DongTai-webapi`负责处理用户的相关操作
- `DongTai-openapi`用于处理`agent`上报的注册/心跳/调用方法/第三方组件/错误日志等数据，下发hook策略，下发探针控制指令等
- `DongTai-engine`根据调用方法数据和污点跟踪算法分析HTTP/HTTPS/RPC请求中是否存在漏洞，同时负责其它相关的定时任务
- `agent`是DongTai的探针模块，包含不同编程语言的数据采集端，用于采集应用运行时的数据并上报至`DongTai-OpenAPI`服务
- `DongTai-deploy`用于洞态IAST的部署，包括docker-compose单节点部署、Kubernetes集群部署等，如果想要更多部署方案，可以提feature申请或贡献部署方案
- `DongTai-Base-Image`包含洞态运行时依赖的基础服务，包括：MySql、Redis
- `DongTai-Plugin-IDEA`是Java探针对应的IDEA插件，可通过插件直接运行Java探针，直接在IDEA中检测漏洞

## 应用场景
"火线-洞态IAST"的应用场景包括但不限于:

- 嵌入`DevSecOps`流程，实现应用漏洞的自动化检测/第三方组件梳理/第三方组件漏洞检测
- 针对开源软件/开源组件进行通用漏洞挖掘
- 上线前安全测试等

## 快速开始
`洞态IAST`支持**SaaS服务**和**本地化部署**，本地化部署的详细部署方案见[**部署文档**](https://github.com/HXSecurity/dongtai-deploy)

### 1. SaaS版本
  - 填写[在线问卷](https://jinshuju.net/f/I9PNmf)注册账号
  - 登录[洞态IAST](https://iast.huoxian.cn)系统
  - 根据[在线文档](https://hxsecurity.github.io/DongTai-Doc/#/doc/tutorial/quickstart?id=%e5%9c%a8%e7%ba%bf%e9%9d%b6%e5%9c%ba-%e5%bf%ab%e9%80%9f%e4%bd%93%e9%aa%8ciast)进行快速体验

### 2. 本地化部署版本【针对联合共建的企业进行开源】

> 本地化部署版本需要自行申请，申请方式见下文

**洞态IAST**支持多种部署方案，可通过[部署文档](https://github.com/HXSecurity/dongtai-deploy)了解部署方案详情，方案如下：

- 单机版部署
  - [x] [docker-compose部署](https://github.com/HXSecurity/dongtai-deploy/tree/main/docker-compose)
  - [ ] docker部署方案 - 待更新
- 集群版部署
  - [x] [Kubernetes集群部署](https://github.com/HXSecurity/dongtai-deploy/tree/main/kubernetes)

#### docker-compose部署
```shell script
$ git clone https://github.com/HXSecurity/DongTai.git
$ cd DongTai
$ chmod u+x build_with_docker_compose.sh
$ ./build_with_docker_compose.sh
```

#### 申请方式
洞态IAST合作伙伴计划—整体开源联合开发，[报名地址](https://jinshuju.net/f/PKPl99)

## 贡献
欢迎并非常感谢您的贡献, 请参阅[contribution.md](https://github.com/HXSecurity/DongTai/blob/main/CONTRIBUTING.md)了解如何向项目贡献


## 文档
- [官方文档](https://hxsecurity.github.io/DongTai-Doc)
- [官方网站](https://iast.huoxian.cn)
