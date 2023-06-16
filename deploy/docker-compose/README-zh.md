## docker-compose一键部署【单机】
[English](README.MD)

洞态IAST云端支持通过`docker-compose`的方式进行一键安装，但是需要提前安装`docker-compose`工具。可以通过`docker-compose -version`命令查看当前机器是否已经安装，如果没有安装，通过百度查询并安装`docker-compose`即可。


### 部署流程

#### 自定义配置(可选)
如需修改mysql和redis的配置，需要手动修改 `config-tutorial.ini`文件内的`[mysql]`和`[redis]`部分配置。
修改完成后,在下述的部署过程选择skip相应的组件.

#### 部署

更新代码

```
git pull
```

执行安装

```
./dtctl install 
```
最新发布版本


```
./dtctl install -v 1.12.0
```
s: 跳过的资源(skip)，可选： `mysql` `redis`  `mysql,redis`，默认：不跳过

v: 需要被安装的版本,默认为最新的发布版本

环境启动成功后，通过安装过程中指定的`web service port`访问即可。


### 升级

更新代码 (每次升级必须执行步骤)
```
git pull
```

执行更新
```
./dtctl upgrade 
```
更新成最新发布版本


```
./dtctl upgrade  -t 1.12.0
```
更新到执行的版本

t: to version 



### 卸载

```
./dtctl rm -d
```
d : 改选项会让数据和服务一起被删除
