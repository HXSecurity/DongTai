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

用法:  
```
./install.sh -m NodePort -s mysql -n dongtai-iast
```

m: 访问模式(mode)，可选：`NodePort` `LoadBalancer`,默认为：NodePort

s: 跳过的资源(skip)，可选： `mysql` `redis`  `mysql,redis`，默认：不跳过

n: 指定namespace，默认为：`dongtai-iast`

## 自定义配置
如需修改mysql和redis的配置，需要手动修改 `manifest/4.deploy-iast-server.yml`最上部分的`[mysql]`和`redis`部分配置。

> 说明：假设`mysql`和`redis`的配置可用于生产环境，此部署方案即可用于生产环境部署。

   
## 访问

### NodePort 

#### 获取可用的Node IP
```shell script
kubectl get nodes -o wide |  awk {'print $1" " $2 " " $7'} | column -t
```

#### 获取可用的NodePort

```shell script
kubectl get svc dongtai-web-pub-svc -n dongtai-iast -o=jsonpath='{.spec.ports[0].nodePort}'
kubectl get svc dongtai-engine-pub-svc -n dongtai-iast -o=jsonpath='{.spec.ports[0].nodePort}')
```

#### 访问地址:
```shell script
http://${NodeIP}:${PORT}
```

### LoadBalancer

#### 获取可用的LoadBalancer IP或者DNS
```shell script
kubectl get svc dongtai-web-pub-svc dongtai-engine-pub-svc -n dongtai-iast
```

## 卸载

```shell script
kubectl delete namespace ${YourNamespace}
```


