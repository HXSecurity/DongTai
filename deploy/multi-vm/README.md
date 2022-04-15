# 三虚拟机部署方案

## 准备

提前准备3台虚拟机，配置如下：

- 操作系统：Ubuntu
- CPU核数：8
- 内存：16G

> 其他可以安装 `Docker` 和 `docker-compose` 的 `Linux` 发行版也可以，这里以 `Ubuntu` 为例。

各个节点部署的内容和IP地址如下：

<table>
    <tr>
        <td>节点</td>
        <td>组件</td>
        <td>IP</td>
    </tr>
    <tr>
        <td>vm1 </td>
        <td>
            dongtai-mysql <br/>
            dongtai-web  <br/>
            dongtai-redis
        </td>
        <td> ip_vm1   </td>
    </tr>
    <tr>
        <td>vm2 </td>
        <td>dongtai-server </td>
        <td> ip_vm2  </td>
    </tr>
    <tr>
        <td>vm3 </td>
        <td>
            dongtai-engine <br/>
            dongtai-engine-task
        </td>
        <td> ip_vm3 </td>
    </tr>
</table>

每个节点上的组件都是通过 `docker-compose` 部署，目录 `vm1` 用于在节点 `vm1` 上安装对应的组件，目录 `vm2` 和目录 `vm3` 类似。目录结构如下：

```shell
multi-vm
├── README.md
├── config-tutorial.ini
├── vm1
│   ├── docker-compose.yml
│   └── nginx.conf
├── vm2
│   ├── docker-compose.yml
│   └── lb.conf
└── vm3
    ├── docker-compose.yaml
    └── lb.conf
```

## 安装步骤

### 1.修改配置

#### 获取最新镜像版本

`./deploy/latest_image.sh`

> 文件内容`{{ }}` 的是需要修改的部分

需要修改的文件如下:

1. `config-tutorial.ini`
2. `vm1/nginx.conf`
3. `vm1/docker-compose.yml`
4. `vm2/docker-compose.yml`
5. `vm3/docker-compose.yml`

### 2.部署 vm1

```shell
cd multi-vm/vm1
docker-compose up -d
```

### 3.部署 vm2

执行安装，扩容成4个副本（可修改）

```shell
cd multi-vm/vm2
docker-compose up --scale dongtai-server=4 -d
```

### 4.部署 vm3

执行安装，扩容成4个副本（可修改）

```shell
cd multi-vm/vm3
docker-compose up --scale dongtai-engine=4 -d
```

## 备份、恢复数据

> Dongtai Server 生产环境推荐用户使用自行维护的数据库，使用默认的 `docker-compose` 内置数据库有**数据丢失风险**。

### vm1 中 docker-compose 内置的 dongtai-mysql 数据库

#### 导出备份

```shell
docker exec -i $(docker ps | grep "dongtai-mysql:" | awk '{print $1}') /bin/bash -c "mysqldump -uroot -pdongtai-iast --single-transaction -R -E --default-character-set=utf8mb4 --databases 'dongtai_webapi' " > dongtai-backup-20220415.sql
```

#### 导入恢复

```shell
docker exec -i $(docker ps | grep "dongtai-mysql:" | awk '{print $1}') /bin/bash -c "mysql -uroot -pdongtai-iast --default-character-set=utf8mb4 dongtai_webapi " < dongtai-backup-20220415.sql
```

### **（推荐）** 用户自行维护的数据库

按照用户自定义的数据和恢复备份、快照策略实施即可。

## 升级

1. 备份数据；
2. 在 [Dongtai-Base-Image](https://github.com/HXSecurity/Dongtai-Base-Image/tree/main/mysql) 获取对应版本增量的 `sql`，执行 `sql` 的命令参考 [导入恢复](#导入恢复)；
3. 修改`vm1` `vm2` `vm3` 中 `docker-compose.yml` 对应镜像的版本，[获取最新镜像版本](#获取最新镜像版本);
