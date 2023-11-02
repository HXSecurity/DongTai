## Deploy With Docker-Compose
[中文版本(Chinese version)](README-zh.md)

## Prepare in advance
  - Docker
  - docker-compose
  - You can verify docker/docker-compose with this command: `docker -v` and `docker-compose`, if you re


### Deployment

#### Custom Configuration(Optional)
If you want to modify the configuration of mysql and redis, you need to modify section `[mysql]` and section`[redis]` of the file `config-tutorial.ini` manually.
After modification, `skip` the relevant component in your deploy step.


#### Deploy

get the latest code

```
git pull
```

install

```
./dtctl install
```

install the latest release version

```
./dtctl install -v 1.16.0
```

s: skip specified component，optional： `mysql` `redis`  `mysql,redis`，default：don't skip

v: the version you want to install, default: latest release version


After installation, access it with your specified `web service port`.




### Upgrade

download latest `dtctl`

```
git pull
```

upgrade

```
./dtctl upgrade
```

upgrade to the latest release version

```
./dtctl upgrade -t 1.16.0
```

upgrade to the specified version

t: to version 



### Uninstall

```
./dtctl rm -d
```
d : remove server and data
