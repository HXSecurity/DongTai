## docker-compose一键部署
洞态IAST云端支持通过`docker-compose`的方式进行一键安装，但是需要提前安装`docker-compose`工具。可以通过`docker-compose -versin`查看当前机器是否已经安装，如果没有安装，通过百度查询`docker-compose`的安装方式进行安装即可。


### 部署流程

**1.修改`config-tutorial.ini`配置文件**
1.1 查看当前机器的内网IP地址：`ifconfig`

1.2 修改`config-tutorial.ini`文件，将**dongtai-openapi**修改为**内网IP**地址

**2.使用`docker-compose`启动环境**
```bash
$ docker-compose up -d
```
环境启动成功后，通过80端口即可访问**WEB**服务

