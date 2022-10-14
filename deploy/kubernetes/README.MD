# Setup in Kubnernetes

[中文版本(Chinese version)](README.ZH-CN.MD)

## Prepare in advance

- Kubernetes version: 1.9+
- Kubectl has been installed on the client
- You can use `kubectl auth can-i` if you have authorization for the following operations：
    - create secrets
    - create deployments
    - create configmaps
    - create namespaces
    - create StatefulSet
    - create Service

## Deployment

### Setup with helm

Before install, you have to make sure the helm is available. Follow [this guide](https://helm.sh/docs/intro/install/) to install helm.

1. Add and update helm chart repo for `Dongtai Iast`

   ```
   helm repo add dongtai https://charts.dongtai.io/iast
   helm repo update
   ```

2. Need to specify your `storageclass`, or specify a public write `pvc`

   ```
   --set storage.storageClassName=storageclass
   or
   --set storage.persistentVolumeClaim=pvc
   ```
   
2. Install

   ```
   helm install ProjectName --create-namespace -n dongtai dongtai/dongtai-iast \
   --set storage.persistentVolumeClaim=pvc
   ```
   
   This command will deploy dongtai servers in dongtai namespace and expose service with `ClusterIP`.

#### Custom configuration

If you want to modify the configuration of mysql and Redis,you can overwrite the values by your own file,Suppose you have a file in `/tmp/my-values.yml` with values as follow:

``` yaml
skipMysql: true
mysql:
  host: my-dongtai-mysql
  port: 3306
  name: my-dongtai_webapi
  user: root
  password: my-dongtai-iast

skipRedis: true
redis:
  host: my-dongtai-redis
  port: 6379
  password: 123456
  db: 0
```

``` shell script
helm install ProjectName --create-namespace -n dongtai dongtai/dongtai-iast --values /tmp/my-values.yaml
```

You can also pass in a single value using **`--set`**, for example, you can switch defalut access type `ClusterIP` to `NodePort` 

```shell
helm install ProjectName --create-namespace -n dongtai dongtai/dongtai-iast \
--set storage.persistentVolumeClaim=pvc \
--set accessType=NodePort --set NodePort=30080 \
--set tag=1.8.5
```

If you need to modify somaxconn (128) 

```
 helm install ProjectName --create-namespace -n dongtai dongtai/dongtai-iast \
 --set storage.persistentVolumeClaim=pvc \
 --set somaxconn=1024
```

Avaliable values:

**skipMysql**:  false (default)
**skipRedis**: false (default)
**accessType**: ClusterIP(default), Options: ClusterIP,NodePort,LoadBalancer
**imageVersion**: latest (default)
**logging_level**: INFO (default)

#### Uninstall
```
helm uninstall ProjectName -n dongtai
```

<img src="https://static.scarf.sh/a.png?x-pxid=a7858f70-7435-420a-bc4e-0b71a7727c99" />


### Scale

With `kubectl scale` command, you can scale `dongtai` deployment to your desire count.

```
kubectl scale deployments ${deployment-names} --replicas=${count} -n ${your-namespace}
```



If you need the yaml file to be deployed directly, please use the following command to export

```
helm install --dry-run ProjectName -n default dongtai/dongtai-iast
```

