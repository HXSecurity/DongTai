# DongTai

[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![license Apache-2.0](https://img.shields.io/github/license/HXSecurity/DongTai-agent-java)](https://github.com/HXSecurity/DongTai-agent-java/blob/main/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/HXSecurity/DongTai?label=DongTai)](https://github.com/HXSecurity/DongTai/releases)

[![GitHub release](https://img.shields.io/github/v/release/HXSecurity/Dongtai-webapi?label=Dongtai-webapi)](https://github.com/HXSecurity/DongTai-webapi/releases)
[![GitHub release](https://img.shields.io/github/v/release/HXSecurity/Dongtai-openapi?label=Dongtai-openapi)](https://github.com/HXSecurity/DongTai-openapi/releases)
[![GitHub release](https://img.shields.io/github/v/release/HXSecurity/Dongtai-engine?label=Dongtai-engine)](https://github.com/HXSecurity/DongTai-engine/releases)
[![GitHub release](https://img.shields.io/github/v/release/HXSecurity/Dongtai-web?label=Dongtai-web)](https://github.com/HXSecurity/DongTai-web/releases)
[![GitHub release](https://img.shields.io/github/v/release/HXSecurity/DongTai-agent-java?label=DongTai-agent-java)](https://github.com/HXSecurity/DongTai-agent-java/releases)
[![GitHub release](https://img.shields.io/github/v/release/HXSecurity/DongTai-agent-python?label=DongTai-agent-python)](https://github.com/HXSecurity/DongTai-agent-python/releases)

[English](README.md)

## DongTai是什么?

洞态IAST是一款开源的交互式安全测试(IAST)产品，可通过被动插桩模式实现JAVA应用的通用漏洞及第三方组件漏洞的实时检测，非常适合在开发流水线的测试阶段使用。

## 项目结构

```
.
├── deploy
├── dongtai_common 各个服务调用的常用函数和类
├── dongtai_conf 配置文件
├── dongtai_engine 漏洞检测与漏洞处理部分
├── dongtai_protocol dongtai-server和agent交互的协议
├── dongtai_web 与web交互的api
├── static 静态文件
└── test 测试用例
```


## 技术架构

"火线-洞态IAST"具有多个基础服务，包括：`DongTai-web`、`DongTai`、 `agent`、`DongTai-Base-Image`、`DongTai-Plugin-IDEA`，其中：

- `DongTai-web`是DongTai的产品页面，用于处理用户与洞态的交互
- `DongTai>>dongtai_web`负责处理用户的相关操作的API
- `DongTai>>dongtai_protocol`用于处理`agent`上报的注册/心跳/调用方法/第三方组件/错误日志等数据，下发hook策略，下发探针控制指令等
- `DongTai>>dongtai_engine` 根据调用方法数据和污点跟踪算法分析HTTP/HTTPS/RPC请求中是否存在漏洞，同时负责其它相关的定时任务
- `agent`是DongTai的探针模块，包含不同编程语言的数据采集端，用于采集应用运行时的数据并上报至`DongTai-OpenAPI`服务
- `DongTai-Base-Image`包含洞态运行时依赖的基础服务，包括：MySql、Redis
- `DongTai-Plugin-IDEA`是Java探针对应的IDEA插件，可通过插件直接运行Java探针，直接在IDEA中检测漏洞

## 应用场景

"火线-洞态IAST"的应用场景包括但不限于:

- 嵌入`DevSecOps`流程，实现应用漏洞的自动化检测/第三方组件梳理/第三方组件漏洞检测
- 针对开源软件/开源组件进行通用漏洞挖掘
- 上线前安全测试等

## 快速开始

`洞态IAST`支持**SaaS服务**和**本地化部署**，本地化部署的详细部署方案见[**部署文档**](./deploy)

### 1. SaaS版本

- 登录[洞态IAST](https://iast.io)系统
- 根据[在线文档](https://doc.dongtai.io/docs/category/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B/)进行快速体验

### 2. 本地化部署版本

**洞态IAST**支持多种部署方案，可通过[部署文档](./deploy)了解部署方案详情，方案如下：

- 单机版部署
  - [x] [docker-compose部署](./deploy/docker-compose)
  - [ ] docker部署方案 - 待更新
- 集群版部署
  - [x] [Kubernetes集群部署](./deploy/kubernetes)

#### docker-compose部署

```shell script
git clone git@github.com:HXSecurity/DongTai.git
cd DongTai
chmod u+x build_with_docker_compose.sh
./build_with_docker_compose.sh
```

## 贡献

欢迎并非常感谢您的贡献, 请参阅[contribution.md](https://github.com/HXSecurity/DongTai/blob/main/CONTRIBUTING.md)了解如何向项目贡献

## 文档

- [官方文档](https://doc.dongtai.io)
- [官方网站](https://dongtai.io)

## Stats

![Alt](https://repobeats.axiom.co/api/embed/ea6a307f8f06cd1c2a19f2312751eb1706382af8.svg "Repobeats analytics image")
