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

### 使用 helm 安装

安装之前请确保已经安装`helm`.通过下面链接[this guide](https://helm.sh/docs/intro/install/)安装.

1. 添加、更新仓库

   ```
   helm repo add dongtai https://charts.dongtai.io/iast
   helm repo update
   ```

2. 需要准备一个 `storageclass`, 或者一个可公共写的 `pvc` 

   ```
   --set storage.storageClassName=storageclass
   or
   --set storage.persistentVolumeClaim=pvc
   ```
   
2. 安装

   ```
   helm install ProjectName --create-namespace -n dongtai dongtai/dongtai-iast --set storage.persistentVolumeClaim=pvc
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
helm install ProjectName --create-namespace -n dongtai dongtai/dongtai-iast --values /tmp/my-values.yaml
```

你也可以使用 `--set`来覆盖单个值, 例如: 你可以使用 `--set` 将 `ClusterIP` 切换成 `NodePort` 

```shell
helm install ProjectName --create-namespace -n dongtai dongtai/dongtai-iast --set storage.persistentVolumeClaim=pvc --set accessType=NodePort --set NodePort=30080 --set tag=1.8.5
```
如果你需要修改 somaxconn (128) 

```
helm install ProjectName --create-namespace -n dongtai dongtai/dongtai-iast --set storage.persistentVolumeClaim=pvc --set somaxconn=1024
```

可用值:

**skipMysql**:  false (default)
**skipRedis**: false (default)
**accessType**: ClusterIP(default), Options: ClusterIP,NodePort,LoadBalancer
**imageVersion**: latest (default)
**logging_level**: INFO (default)

#### 卸载
```
helm uninstall ProjectName -n dongtai
```


### 扩缩容

使用 `kubectl scale` 命令可以把 `dongtai` 服务扩容成你期望的数量。

```
kubectl scale deployments ${deployment-names} --replicas=${count} -n ${your-namespace}
```



如果需要yaml文件直接部署，请使用如下命令导出

```
helm install --dry-run ProjectName -n default dongtai/dongtai-iast
```

