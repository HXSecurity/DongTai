#!/bin/bash
OUT="$(uname -s)"

Info(){
  echo -e "[Info] $1"
}

Error(){
  echo -e "\033[31m[Error] $1 \033[0m"
}

Todo(){
  echo -e "\033[36m[Todo] $1 \033[0m"
}

Notice(){
  echo -e "\033[33m[Important] $1 \033[0m"
}

CURRENT_PATH=$(cd "$(dirname "$0")" || exit;pwd)

cd "$CURRENT_PATH" || exit


# Check if the Docker service is turned on
check_docker(){
  Info "check docker servie status."
  docker ps 1>/dev/null 2>/dev/null
  
  if [ $? -ne 0 ]; then
    Error "docker service is down. please start docker service and rerun."
    exit
  else
    Info "docker service is up."
  fi
}

login_dongtai_repo(){
  Info "Login to DongTai-Image Repo"
  docker login --username=dongtai-image@huoxian --password DkhcuicgyEzwxBr2MNy2iQ89 registry.cn-beijing.aliyuncs.com
}


check_docker_compose(){
  if ! [ -x "$(command -v docker-compose)" ]; then
    Error 'docker-compose not installed.'
    exit 1
  fi
}

Info "mysql persistence"
mkdir data

start_docker_compose(){
  Info "Starting docker compose ..."
  docker-compose -p dongtai-iast up -d
}


# Specify the port of Web, OpenAPI service and check whether it is available
check_port(){
  Info "check port status"

  read -p "[+] please input web service port, default [80]:" WEB_SERVICE_PORT
  if [ -z $WEB_SERVICE_PORT ];then
    WEB_SERVICE_PORT=80
  fi

  lsof -i:$WEB_SERVICE_PORT|grep "LISTEN" 2>/dev/null
  
  if [ $? -ne 0 ]; then
    Info "port $WEB_SERVICE_PORT is ok."
  else
    Error "port $WEB_SERVICE_PORT is already in use. please change default port."
    exit
  fi

  read -p "[+] please input openAPI service port, default [8000]:" OPENAPI_SERVICE_PORT
  if [ -z $OPENAPI_SERVICE_PORT ];then
    OPENAPI_SERVICE_PORT=8000
  fi
  lsof -i:$OPENAPI_SERVICE_PORT | grep "LISTEN" 2>/dev/null

  if [ $? -ne 0 ]; then
    Info "port $OPENAPI_SERVICE_PORT is ok."
  else
    Error "port $OPENAPI_SERVICE_PORT is already in use. please change default port."
    exit
  fi

  echo '''version: "2"
services:
  dongtai-mysql:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest
    restart: always
    volumes:
      - ./data:/var/lib/mysql:rw

  dongtai-redis:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-redis:latest
    restart: always

  dongtai-webapi:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-webapi:latest
    restart: always
    volumes:
      - $PWD/config-tutorial.ini:/opt/dongtai/webapi/conf/config.ini
    depends_on:
      - dongtai-mysql
      - dongtai-redis

  dongtai-web:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-web:latest
    restart: always
    ports:
      - "'''$WEB_SERVICE_PORT''':80"
    volumes:
      - $PWD/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - dongtai-webapi

  dongtai-openapi:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-openapi:latest
    restart: always
    volumes:
       - $PWD/config-tutorial.ini:/opt/dongtai/openapi/conf/config.ini
    ports:
      - "'''$OPENAPI_SERVICE_PORT''':8000"
    depends_on:
      - dongtai-mysql
      - dongtai-redis

  dongtai-engine:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-engine:latest
    restart: always
    volumes:
      - $PWD/config-tutorial.ini:/opt/dongtai/engine/conf/config.ini
    depends_on:
      - dongtai-mysql
      - dongtai-redis

  dongtai-engine-task:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-engine:latest
    restart: always
    command: ["/opt/dongtai/engine/docker/entrypoint.sh", "task"]
    volumes:
      - $PWD/config-tutorial.ini:/opt/dongtai/engine/conf/config.ini
    depends_on:
      - dongtai-mysql
      - dongtai-redis
      - dongtai-engine''' > docker-compose.yml
}

check_docker
check_docker_compose
login_dongtai_repo
check_port
start_docker_compose

Notice "Installation success!"



