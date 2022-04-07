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

### Setup with shell

Usage:  
```
./install.sh -m NodePort -s mysql -n dongtai-iast
```

m: access mode(mode), optional: `NodePort` `LoadBalancer`, default: NodePort

s: skipped resources(skip), optional: `mysql` `redis`  `mysql,redis`, default: don't skip

n: specify the namespace, default: `dongtai-iast`

#### Custom configuration

If you want to modify the configuration of mysql and Redis, manually modify the configuration `manifest/4.deploy-iast-server.yml` The top part of `[mysql]` and `redis`.

> Note: Assuming that `mysql` and `redis` can be configured for production, this deployment scheme can be used for production deployment.

####  Access

##### NodePort 

##### Obtain an available Node IP address

```shell script
kubectl get nodes -o wide |  awk {'print $1" " $2 " " $7'} | column -t
```

##### Obtain an available NodePort

```shell script
kubectl get svc dongtai-web-pub-svc -n dongtai-iast -o=jsonpath='{.spec.ports[0].nodePort}'
```

##### Access Link:

```shell script
http://${NodeIP}:${PORT}
```

##### LoadBalancer

##### Obtain the available LoadBalancer IP address or DNS

```shell script
kubectl get svc dongtai-web-pub-svc dongtai-engine-pub-svc -n dongtai-iast
```

#### Uninstall

```shell script
kubectl delete namespace ${YourNamespace}
```

### Setup with helm

Before install, you have to make sure the helm is available. Follow [this guide](https://helm.sh/docs/intro/install/) to install helm.

1. Add and update helm chart repo for `Dongtai Iast`

   ```
   helm repo add dongtai https://charts.dongtai.io/iast
   helm repo update
   ```

2. Install

   ```
   helm install --create-namespace -n dongtai  dongtai-iast dongtai/dongtai-iast
   ```
   
   This command will deploy dongtai servers in dongtai namespace and expose service with `ClusterIP`.

#### Custom configuration

If you want to modify the configuration of mysql and Redis,you can overwrite the values by your own file,Suppose you have a file in `/tmp/my-values.yml` with values as follow:

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

You can also pass in a single value using **`--set`**, for example, you can switch defalut access type `ClusterIP` to `NodePort` 

```shell
helm install --create-namespace -n dongtai-test --set accessType=NodePort --set imageVersion=1.3.1  dongtai-iast dongtai/dongtai-iast

```

Avaliable values:

**skipMysql**:  false (default)
**skipRedis**: false (default)
**accessType**: ClusterIP(default), Options: ClusterIP,NodePort,LoadBalancer
**imageVersion**: latest (default)

#### Uninstall
```
helm uninstall dongtai-iast -n dongtai
```

<img src="https://static.scarf.sh/a.png?x-pxid=a7858f70-7435-420a-bc4e-0b71a7727c99" />


### Scale

With `kubectl scale` command, you can scale `dongtai` deployment to your desire count.

```
kubectl scale deployments ${deployment-names} --replicas=${count} -n ${your-namespace}
```
