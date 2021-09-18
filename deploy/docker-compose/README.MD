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
./install.sh  -s mysql
```
s: skip specified component，optional： `mysql` `redis`  `mysql,redis`，default：don't skip


After installation, access it with your specified `web service port`.
