# DongTai
[![django-project](https://img.shields.io/badge/django%20versions-3.0.3-blue)](https://www.djangoproject.com/)
[![license GPL-3.0](https://img.shields.io/github/license/HXSecurity/DongTai-agent-java)](https://github.com/HXSecurity/DongTai-agent-java/blob/main/LICENSE)
[![DongTai-project](https://img.shields.io/badge/DongTai%20versions-beta-green)](https://github.com/HXSecurity/DongTai)

[![DongTai--webapi](https://img.shields.io/badge/DongTai--webapi-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-webapi)
[![DongTai--openapi](https://img.shields.io/badge/DongTai--openapi-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-openapi)
[![DongTai--engine](https://img.shields.io/badge/DongTai--engine-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-engine)
[![DongTai--web](https://img.shields.io/badge/DongTai--web-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-web)
[![DongTai--agent--java](https://img.shields.io/badge/DongTai----agent--java-v1.0.0-lightgrey)](https://github.com/HXSecurity/DongTai-agent-java)

[中文版本(Chinese version)](README.ZH-CN.MD)

## What is DongTai?
DongTai is an open-source passive interactive security testing (IAST) product. It uses dynamic hooks and taint tracking algorithms to achieve **universal vulnerability detection** and **multiple request associated vulnerability detection (including but not limited to unauthorized vulnerabilities, overpower vulnerabilities)**, **Third-party component vulnerability detection**, etc. Currently, applications in Java and Python are supported for vulnerability detection.

## Architecture 
"huoxian-DongTai IAST" has multiple basic services, including: `DongTai-web`, `DongTai-webapi`, `DongTai-openapi`, `DongTai-engine`, `agent`, `DongTai-deploy`, ` DongTai-Base-Image`, `DongTai-Plugin-IDEA`, among them:
- `DongTai-web` is the product page of DongTai, which is used to handle the interaction between users and cave states
- `DongTai-webapi` is responsible for handling user-related operations
- `DongTai-openapi` is used to process the registration/heartbeat/call method/third-party component/error log data reported by `agent`, issue hook strategy, issue probe control commands, etc
- `DongTai-engine` analyzes whether there are vulnerabilities in HTTP/HTTPS/RPC requests according to the calling method data and taint tracking algorithm, and is also responsible for other related timing tasks
- `agent` is a probe module of DongTai, including data collection terminals in different programming languages, used to collect data during application runtime and report to the `DongTai-OpenAPI` service
- `DongTai-deploy` is used for the deployment of DongTai IAST, including docker-compose single-node deployment, Kubernetes cluster deployment, etc. If you want a deployment plan, you can add features or contribute to the deployment plan
- `DongTai-Base-Image` contains the basic services that DongTai depends on at runtime, including: MySql, Redis
- `DongTai-Plugin-IDEA` is the IDEA plug-in corresponding to the Java probe. You can run the Java probe directly through the plug-in and detect the vulnerabilities directly in IDEA.

## scenario
The usage scenarios of "huoxian-DongTai IAST" include but are not limited to:

- Embed the `DevSecOps` process to realize automatic detection of application vulnerabilities/third-party component combing/third-party component vulnerability detection
- General vulnerability mining for open source software/open source components
- Safety test before going live, etc.

## Quick start
`Dong State IAST` supports **SaaS service** and **localized deployment**. For the detailed deployment plan of localized deployment, please refer to [**Deployment Document**](https://github.com/HXSecurity/ dongtai-deploy)

### 1. SaaS version
  - Fill in the [online questionnaire](https://jinshuju.net/f/I9PNmf) to register an account
  - Log in to the [DongTai IAST] (https://iast.huoxian.cn) system
  - According to [online documentation](https://hxsecurity.github.io/DongTaiDoc/#/doc/tutorial/quickstart?id=%e5%9c%a8%e7%ba%bf%e9%9d%b6%e5%9c%ba-%e5%bf%ab%e9%80%9f%e4%bd%93%e9%aa%8ciast) for a quick experience

### 2. Localized deployment version [open source for companies jointly built]

> You need to apply for the localized deployment version by yourself, see below for how to apply

**DongTai IAST** supports a variety of deployment schemes. You can learn more about the deployment scheme through [Deployment Document](https://github.com/HXSecurity/dongtai-deploy), the scheme is as follows:

- Stand-alone deployment
  - [x] [docker-compose](https://github.com/HXSecurity/dongtai-deploy/tree/main/docker-compose)
  - [ ] docker - pending upgrade
- Cluster deployment
  - [x] [Kubernetes](https://github.com/HXSecurity/dongtai-deploy/tree/main/kubernetes)

#### docker-compose
```shell script
$ git clone https://github.com/HXSecurity/DongTai.git
$ cd DongTai
$ chmod u+x build_with_docker_compose.sh
$ ./build_with_docker_compose.sh
```

#### How to apply
DongTai IAST partner program-overall open source joint development, [registration address](https://jinshuju.net/f/PKPl99)

## Contributing
Contributions are welcomed and greatly appreciated. See [CONTRIBUTING.md](https://github.com/HXSecurity/DongTai/blob/main/CONTRIBUTING.md) for details on submitting patches and the contribution workflow.

Any questions? Let's discuss in [#DongTai discussions](https://github.com/HXSecurity/DongTai/discussions)

## More resources
- [Documentation](https://hxsecurity.github.io/DongTai-Doc)
- [DongTai WebSite](https://iast.huoxian.cn)
