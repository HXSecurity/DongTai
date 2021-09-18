#!/bin/bash
SKIP_MYSQL=false
SKIP_REDIS=false

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


while getopts ":m:s:n:h" optname
do
    case "$optname" in
      "s")
        SKIP=$OPTARG
        array=(${SKIP//,/ })
        for var in "${array[@]}"
          do
            if [ "$var" == "mysql" ]; then
              SKIP_MYSQL=true
            elif [ "$var" == "redis" ]; then
              SKIP_REDIS=true
            fi
          done
        ;;
      "h")
        Info "Usage: ./install.sh -s mysql"
        exit 1
        ;;
      ":")
        Error "No argument value for option $OPTARG"
        ;;
      "?")
        Error "Unknown option $OPTARG"
        ;;
      *)
        Error "Unknown error while processing options"
        ;;
    esac
done

OUT="$(uname -s)"
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
}

create_docker_compose_file(){
MYSQL_STR=""
REDIS_STR=""
if [ $SKIP_MYSQL == false ]; then
  export MYSQL_STR=`cat <<EOF;
dongtai-mysql: 
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest
    restart: always
    volumes:
      - ./data:/var/lib/mysql:rw

EOF
`
fi

if [ $SKIP_REDIS == false ]; then
  export REDIS_STR=`cat <<EOF;
dongtai-redis:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-redis:latest
    restart: always

EOF
`
fi

cat > docker-compose.yml <<EOF
version: "2"
services:
  $MYSQL_STR
  $REDIS_STR
  dongtai-webapi:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-webapi:latest
    restart: always
    volumes:
      - \$PWD/config-tutorial.ini:/opt/dongtai/webapi/conf/config.ini

  dongtai-web:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-web:latest
    restart: always
    ports:
      - "$WEB_SERVICE_PORT:80"
    volumes:
      - \$PWD/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - dongtai-webapi

  dongtai-openapi:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-openapi:latest
    restart: always
    volumes:
       - \$PWD/config-tutorial.ini:/opt/dongtai/openapi/conf/config.ini
    ports:
      - "$OPENAPI_SERVICE_PORT:8000"

  dongtai-engine:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-engine:latest
    restart: always
    volumes:
      - \$PWD/config-tutorial.ini:/opt/dongtai/engine/conf/config.ini


  dongtai-engine-task:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-engine:latest
    restart: always
    command: ["/opt/dongtai/engine/docker/entrypoint.sh", "task"]
    volumes:
      - \$PWD/config-tutorial.ini:/opt/dongtai/engine/conf/config.ini
    depends_on:
      - dongtai-engine
EOF
}

check_docker
check_docker_compose
login_dongtai_repo
check_port
create_docker_compose_file
start_docker_compose

Notice "Installation success!"
