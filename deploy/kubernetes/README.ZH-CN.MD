# Kubnernetes环境快速部署
[English](README.MD)

## 提前准备

- Kubernetes 版本：1.9+
- 客户端已经安装kubectl
- 具备以下操作的授权,可以使用`kubectl auth can-i`验证：
    - create secrets
    - create deployments
    - create configmaps
    - create namespaces
    - create StatefulSet
    - create Service

## 部署

### 脚本安装

用法:  
```
./install.sh -m NodePort -s mysql -n dongtai-iast
```

m: 访问模式(mode)，可选：`NodePort` `LoadBalancer`,默认为：NodePort

s: 跳过的资源(skip)，可选： `mysql` `redis`  `mysql,redis`，默认：不跳过

n: 指定namespace，默认为：`dongtai-iast`

#### 自定义配置

如需修改mysql和redis的配置，需要手动修改 `manifest/4.deploy-iast-server.yml`最上部分的`[mysql]`和`redis`部分配置。

> 说明：假设`mysql`和`redis`的配置可用于生产环境，此部署方案即可用于生产环境部署。


####  访问

##### NodePort 

##### 获取可用的Node IP
```shell script
kubectl get nodes -o wide |  awk {'print $1" " $2 " " $7'} | column -t
```

#### 获取可用的NodePort

```shell script
kubectl get svc dongtai-web-pub-svc -n dongtai-iast -o=jsonpath='{.spec.ports[0].nodePort}'
```

##### 访问地址:
```shell script
http://${NodeIP}:${PORT}
```

##### LoadBalancer

##### 获取可用的LoadBalancer IP或者DNS
```shell script
kubectl get svc dongtai-web-pub-svc dongtai-engine-pub-svc -n dongtai-iast
```

####  卸载

```shell script
kubectl delete namespace ${YourNamespace}
```


### 使用 helm 安装

安装之前请确保已经安装`helm`.通过下面链接[this guide](https://helm.sh/docs/intro/install/)安装.

1. 添加、更新仓库

   ```
   helm repo add dongtai https://charts.dongtai.io/iast
   helm repo update
   ```

2. 安装

   ```
   helm install --create-namespace -n dongtai  dongtai-iast dongtai/dongtai-iast
   ```
   
   这个命令将会在dongtai命名空间部署 `Dongtai` 服务,并且使用 `ClusterIP` 方式暴露服务.

#### 自定义配置

如果需要自定义mysql和redis的配置,你可以使用自己的文件覆盖默认的values文件.
假如你有一个自定义文件 `/tmp/my-values.yml` 如下:

``` yaml
mysql:
  host: my-dongtai-mysql
  port: 3306
  name: my-dongtai_webapi
  user: root
  password: my-dongtai-iast

redis:
  host: my-dongtai-redis
  port: 6379
  password: 123456
  db: 0
```

``` shell script
 helm install --create-namespace -n dongtai --values /tmp/my-values.yaml dongtai-iast dongtai/dongtai-iast
```

你也可以使用 `--set`来覆盖单个值, 例如: 你可以使用 `--set` 将 `ClusterIP` 切换成 `NodePort` 

```shell
helm install --create-namespace -n dongtai-test --set accessType=NodePort --set imageVersion=1.3.1  dongtai-iast dongtai/dongtai-iast
```
可用值:

**skipMysql**:  false (default)
**skipRedis**: false (default)
**accessType**: ClusterIP(default), Options: ClusterIP,NodePort,LoadBalancer
**imageVersion**: latest (default)

#### 卸载
```
helm uninstall dongtai-iast -n dongtai
```


### 扩缩容

使用 `kubectl scale` 命令可以把 `dongtai` 服务扩容成你期望的数量。

```
kubectl scale deployments ${deployment-names} --replicas=${count} -n ${your-namespace}
```