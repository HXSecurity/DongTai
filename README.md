# 洞态IAST ～ WEBAPI

## 业务简介
- 项目管理
- 漏洞管理
- 组件管理
- 系统配置
- 用户/角色管理
    - 部门管理（新增/修改/删除）
    - 用户管理（新增/修改/删除）
- Agent部署
- 租户管理
    - 新增租户


### SAAS版数据API
> 功能：
> 1. 接收agent返回的方法池数据
> 2. 数据存储
> 3. 加载数据, 并根据指定的方法条件进行搜索

- 策略自定义（hook策略）
- 漏洞匹配策略

#### 部署方案
- 源码部署
- 容器部署

**源码部署**

1.初始化数据库

- 安装MySql 5.7，创建数据库`dongtai-webapi`，运行数据库文件`conf/db.sql`
- 进入`webapi`目录，运行`python manage.py createsuperuser`命令创建管理员

2.修改配置文件

- 复制配置文件`conf/config.ini.example`为`conf/config.ini`并需改其中的配置；其中，`engine`对应的url为`dongtai-engine`的服务地址，`apiserver`对应的url为`dongtai-openapi`的服务地址

3.运行服务 

- 运行`python manage.py runserver`启动服务
