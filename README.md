# DongTai
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![license GPL-3.0](https://img.shields.io/github/license/HXSecurity/DongTai-agent-java)](https://github.com/HXSecurity/DongTai-agent-java/blob/main/LICENSE)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://github.com/HXSecurity/DongTai)
[![DongTai--webapi](https://img.shields.io/badge/DongTai--webapi-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-webapi)
[![DongTai--openapi](https://img.shields.io/badge/DongTai--openapi-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-openapi)
[![DongTai--engine](https://img.shields.io/badge/DongTai--engine-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-engine)
[![DongTai--web](https://img.shields.io/badge/DongTai--web-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-web)
[![DongTai--agent--java](https://img.shields.io/badge/DongTai----agent--java-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-agent-java)

## 一、项目介绍

“火线～洞态IAST”是一款专为甲方安全人员、代码审计工程师和0 Day漏洞挖掘人员量身打造的辅助工具，可用于集成devops环境进行漏洞检测、作为代码审计的辅助工具和自动化挖掘0 Day。

“火线～洞态IAST”具有五大模块，分别是`DongTai-webapi`、`DongTai-openapi`、`DongTai-engine`、`DongTai-web`、`agent`，其中：
- `DongTai-webapi`用于与`DongTai-web`交互，负责页面相关的API请求；
- `DongTai-openapi`用于与`agent`交互，处理agent上报的数据，向agent下发策略，控制agent的运行等
- `DongTai-engine`用于对`DongTai-openapi`接收到的数据进行分析、处理，计算存在的漏洞和可用的污点调用链等
- `DongTai-web`为“火线～洞态IAST”的前端项目，负责页面展示
- `agent`为各语言的数据采集端，从安装探针的项目中采集相对应的数据，发送至`DongTai-openapi`服务

## 二、应用场景
“火线～洞态IAST”可应用于：`devsecops`阶段做自动化漏洞检测、开源软件/组件挖掘通用漏洞、上线前安全测试等场景，主要目的是降低现有漏洞检测的工作量，释放安全从业人员的生产力来做更专业的事情。

## 三、快速开始
`洞态IAST`提供**SaaS版本**、**本地化部署版本**，详细部署方案见：[**部署文档**](https://github.com/HXSecurity/dongtai-deploy)

### 1. SaaS版本
  - 填写[在线问卷](https://wj.qq.com/s2/8269653/6ff2/)注册账号
  - 登录[洞态IAST](https://iast.huoxian.cn/login)系统
  - 根据[在线文档](https://hxsecurity.github.io/DongTaiDoc/#/doc/tutorial/quickstart?id=%e5%9c%a8%e7%ba%bf%e9%9d%b6%e5%9c%ba-%e5%bf%ab%e9%80%9f%e4%bd%93%e9%aa%8ciast)进行快速体验

### 2. 本地化部署版本【针对联合共建的企业进行开源】

本地化部署版本需要自行申请，申请方式见下文

**洞态IAST**云端支持多种部署方案，可通过[部署文档](https://github.com/HXSecurity/dongtai-deploy)了解部署方案详情，方案如下：

- 单机版部署
  - [x] [docker-compose一键部署](https://github.com/HXSecurity/dongtai-deploy/tree/main/docker-compose)
  - [x] [源码一键部署](https://github.com/HXSecurity/dongtai-deploy#3-%E6%BA%90%E7%A0%81%E4%B8%80%E9%94%AE%E9%83%A8%E7%BD%B2)
  - [ ] docker一键部署方案待更新
- 集群版部署
  - [x] [Kubernetes一键部署](https://github.com/HXSecurity/dongtai-deploy/tree/main/kubernetes)

#### docker-compose一键部署

参与联合共建的企业可直接使用如下方式进行部署

```shell script
$ git clone https://github.com/HXSecurity/DongTai.git
$ cd DongTai
$ chmod u+x build_with_docker_compose.sh
$ ./build_with_docker_compose.sh
```

#### 申请方式
洞态IAST合作伙伴计划—整体开源联合开发，[报名地址](https://jinshuju.net/f/PKPl99)

## 四、文档
- [官方文档](https://hxsecurity.github.io/DongTaiDoc/#/doc/tutorial/quickstart)
- [快速体验](https://iast.huoxian.cn)
