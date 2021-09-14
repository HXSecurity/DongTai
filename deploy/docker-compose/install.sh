#!/bin/bash
OUT="$(uname -s)"


CURRENT_PATH=$(cd "$(dirname "$0")" || exit;pwd)

cd "$CURRENT_PATH" || exit

login_dongtai_repo(){
  echo "Login to DongTai-Image Repo"
  docker login --username=dongtai-image@huoxian --password DkhcuicgyEzwxBr2MNy2iQ89 registry.cn-beijing.aliyuncs.com
}

check_env(){
  if ! [ -x "$(command -v docker-compose)" ]; then
    echo '[Error] docker-compose not installed.'
    exit 1
  fi
}

echo "mysql persistence"
mkdir data

start_docker_compose(){
  echo "[Info] Starting docker compose ..."
  docker-compose -p dongtai-iast up -d
}


check_env
login_dongtai_repo
start_docker_compose

echo "[Info] Installation success!"



