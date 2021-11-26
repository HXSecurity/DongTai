## Deploy With Docker-Compose
[中文版本(Chinese version)](README.ZH-CN.MD)

## Prepare in advance
  - Docker
  - docker-compose
  - You can verify docker/docker-compose with this command: `docker -v` and `docker-compose`, if you re


### Deployment

#### Custom Configuration(Optional)
If you want to modify the configuration of mysql and redis, you need to modify section `[mysql]` and section`[redis]` of the file `config-tutorial.ini` manually.
After modification, `skip` the relevant component in your deploy step.

#### Deploy

```
./dtctl install -v 1.0.5 -s mysql
```
s: skip specified component，optional： `mysql` `redis`  `mysql,redis`，default：don't skip

v: the version you want to install


After installation, access it with your specified `web service port`.




### Upgrade

```
./dtctl upgrade -f 1.0.5 -t 1.1.2
```

f: from version
t: to version 


### Uninstall

```
./dtctl rm -d
```
d : remove server and data