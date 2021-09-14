# Rapid deployment of Kubnernetes environment

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

Usage:  
```
./install.sh -m NodePort -s mysql -n dongtai-iast
```

m: access mode(mode), optional: `NodePort` `LoadBalancer`, default: NodePort

s: skipped resources(skip), optional: `mysql` `redis`  `mysql,redis`, default: don't skip

n: specify the namespace, default: `dongtai-iast`

## custom configuration

If you want to modify the configuration of mysql and Redis, manually modify the configuration `manifest/4.deploy-iast-server.yml` The top part of `[mysql]` and `redis`.

> Note: Assuming that `mysql` and `redis` can be configured for production, this deployment scheme can be used for production deployment.

## Access

### NodePort 

#### Obtain an available Node IP address

```shell script
kubectl get nodes -o wide |  awk {'print $1" " $2 " " $7'} | column -t
```

#### Obtain an available NodePort

```shell script
kubectl get svc dongtai-web-pub-svc -n dongtai-iast -o=jsonpath='{.spec.ports[0].nodePort}'
kubectl get svc dongtai-engine-pub-svc -n dongtai-iast -o=jsonpath='{.spec.ports[0].nodePort}')
```

#### Access Link:

```shell script
http://${NodeIP}:${PORT}
```

### LoadBalancer

#### Obtain the available LoadBalancer IP address or DNS

```shell script
kubectl get svc dongtai-web-pub-svc dongtai-engine-pub-svc -n dongtai-iast
```

## Uninstall

```shell script
kubectl delete namespace ${YourNamespace}
```


