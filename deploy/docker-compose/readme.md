## docker-compose一键部署【单机】
洞态IAST云端支持通过`docker-compose`的方式进行一键安装，但是需要提前安装`docker-compose`工具。可以通过`docker-compose -version`命令查看当前机器是否已经安装，如果没有安装，通过百度查询并安装`docker-compose`即可。


### 部署流程

1. 查看当前机器的内网IP地址：`ifconfig`，如：192.168.1.101

2. 执行`install.sh`启动环境安装。用法: `./install.sh <ip>`, 例如：

    ```shell script
       ./install.sh 192.168.1.101
    ```
    
环境启动成功后，通过80端口访问即可。

