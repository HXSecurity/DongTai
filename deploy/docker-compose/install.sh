#!/bin/bash
if [[ -z "$1" ]] ; then
 echo "Usage: $0 <ip>"
 exit 1
fi

OUT="$(uname -s)"

case "${OUT}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${OUT}"
esac

CURRENT_PATH=$(cd "$(dirname "$0")" || exit;pwd)
IP=$1
CONF=config-tutorial.ini
TEMP=$CONF.temp
OPEN_API="dongtai-openapi"

cd "$CURRENT_PATH" || exit


check_env(){
  if ! [ -x "$(command -v docker-compose)" ]; then
    echo '[Error] docker-compose not installed.'
    exit 1
  fi
}

create_temporary_conf(){
  cp $CONF $TEMP
  echo "[Info] Copying temporary config ..."
  if [ "${machine}" == "Mac" ]; then
    sed -i "" "s/$OPEN_API/$IP/g" $CONF >/dev/null
  elif [ "${machine}" == "Linux" ]; then
    sed -i "s/$OPEN_API/$IP/g" $CONF >/dev/null
  else
      echo "[Error] Unsupported shell version."
      exit 1
  fi
}

start_docker_compose(){
  echo "[Info] Starting docker compose ..."
  docker-compose -p dongtai-iast up -d
}

clean_temporary_conf(){
  echo "[Info] Cleaning temporary config ..."
  cp $TEMP $CONF
  rm $TEMP
}

check_env
create_temporary_conf
start_docker_compose
clean_temporary_conf

echo "[Info] Installation success!"



