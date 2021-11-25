#!/bin/bash
CURRENT_PATH=$(cd "$(dirname "$0")" || exit;pwd)
SHA_FILE=updaterecord.txt
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

Usage(){
  Info "Usage: ./install.sh -from 1.0.5 -to 1.1.0"
}

trim()
{
    local trimmed="$1"
    # Strip leading spaces.
    while [[ $trimmed == ' '* ]]; do
       trimmed="${trimmed## }"
    done
    # Strip trailing spaces.
    while [[ $trimmed == *' ' ]]; do
        trimmed="${trimmed%% }"
    done
    echo "$trimmed"
}

while getopts ":f:t:m:s:n:h" optname
do
    case "$optname" in
      "f")
        FROM_VERSION=$OPTARG
        ;;
      "t")
        TO_VERSION=$OPTARG
        ;;
      "h")
        Info "Usage: ./install.sh -from 1.0.5 -to 1.1.0"
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

function check_param(){
  ParamOk=true
  if [ -z "$FROM_VERSION" ]
   then Error "FROM_VERSION required."
    ParamOk=false
  fi
  if [ -z "$TO_VERSION" ]
    then Error "TO_VERSION required. "
      ParamOk=false
   fi

  if [ ! $ParamOk = true ]
   then
    Usage
    exit
  fi

}

echo "FROM_VERSION:$FROM_VERSION"
echo "TO_VERSION:$TO_VERSION"

OUT="$(uname -s)"

case "${OUT}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${OUT}"
esac


sha=sha1sum
if [ $machine == "Mac" ]
then
  sha=shasum
fi


UPGRADE_DIR=~/dongtai_iast_upgrade
now=$(date '+%Y-%m-%d-%H-%M-%S')
backup_filename=$UPGRADE_DIR/dongtai_iast-$now.sql

MYSQL_CONTAINER_ID=$(docker ps | grep 'dongtai-mysql:' | awk '{print $1}')
WEB_CONTAINER_ID=$(docker ps | grep 'dongtai-web:' | awk '{print $1}')


function backup_mysql(){
  mkdir -p $UPGRADE_DIR
  Info "Start to backup exist data..."
  retval=$(echo "dongtai-iast" |  docker exec -i  $MYSQL_CONTAINER_ID  mysqldump -u root -d dongtai_webapi -p >$backup_filename )
  Info "Finished backup exist data..."

}


function check_update_record_file(){
  if [ ! -f "$SHA_FILE" ]; then
    Error "updaterecord.txt does not exists!" 
    exit
fi
}

function current_hash(){
  retval=""
  retval=$(echo "dongtai-iast" |  docker exec -i  $MYSQL_CONTAINER_ID  mysqldump -u root -d dongtai_webapi --ignore-table=dongtai_webapi.mysql_version_control -p --skip-comments   --skip-opt | sed 's/ AUTO_INCREMENT=[0-9]*//g' | sed 's/\/\*!*.*//g' | $sha |awk '{print $1}')
  echo "$retval" 
}

function check_schema_hash(){
  Info "Check database schema ..."

  # set -x
  # cat updaterecord.txt | awk "{ if($1==$FROM_VERSION) print $4}"

  FROM_DB_HASH=$(cat updaterecord.txt | awk -v FROM_VERSION=$FROM_VERSION '{ if($1==FROM_VERSION) print $4}')
  CURRENT_DATABASE_HASH=$( current_hash )

  Info "FROM_DB_HASH:$FROM_DB_HASH"
  Info "CURRENT_DATABASE_HASH:$CURRENT_DATABASE_HASH"

  if [ ! $CURRENT_DATABASE_HASH == $FROM_DB_HASH ]
  then
    Error "Your current database hash value  not equals to the verison $FROM_VERSION, please check."
    exit
  fi

  Info "Database schema correct ..."
}


function execute_update(){
  # set -x
  # extract sql name and reverse list 
  SQL_NAMES=$(cat updaterecord.txt| awk "/$TO_VERSION/,/$FROM_VERSION/ {print \$2}" | grep -v "$FROM_VERSION" | awk "{array[NR]=\$0} END { for(i=NR;i>0;i--) {print array[i];} }" )

# fetch sql from aliyun OSS
  for SQL in $SQL_NAMES
  do 
    Info "Start to download sql:[$SQL]"
    STATUS=$(curl -o $UPGRADE_DIR/$SQL -w "%{http_code}" https://huoqi-public.oss-cn-beijing.aliyuncs.com/iast/sql/$SQL)
    if [ ! $STATUS == "200" ] 
    then 
      Error "SQL:[$SQL] does not exists in OSS,please contract dongtai administrator."
      exit
    fi
  done

  Info "Success downloaded ${#SQL_NAMES[@]} sqls."


  # sql downloaded,start to execute sql
  for SQL in $SQL_NAMES
  do 
    Info "Start to load sql:[$UPGRADE_DIR/$SQL]"
    Info $SQL
    docker exec -i $MYSQL_CONTAINER_ID mysql -uroot -p"dongtai-iast" dongtai_webapi < $UPGRADE_DIR/$SQL
  done
}

function check_after_execute(){
  Info "Check result..."
  TO_DB_HASH=$(cat updaterecord.txt | awk -v TO_VERSION=$TO_VERSION '{ if($1==TO_VERSION) print $4}')
  CURRENT_DATABASE_HASH=$( current_hash )

  Info "TO_DB_HASH:$TO_DB_HASH"
  Info "CURRENT_DATABASE_HASH:$CURRENT_DATABASE_HASH"

  if [ ! $CURRENT_DATABASE_HASH == $TO_DB_HASH ]
  then
    Error "Your current database hash value  not equals to the verison $TO_DB_HASH, please check."
    exit
  fi

  Info "Current database schema correct ..."
  Info "Upgrade Success ..."
}

function upgrade_docker_image(){
CHANGE_THIS_VERSION=$TO_VERSION
WEB_PORT=$(docker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}} {{(index $conf 0).HostPort}} {{end}}' $WEB_CONTAINER_ID)
WEB_PORT=$(trim $WEB_PORT)


read -r -d '' DOCKER_COMPOSE_FILE << EOM
version: "2"
services:
  dongtai-webapi:
    image: "dongtai.docker.scarf.sh/dongtai/dongtai-webapi:$CHANGE_THIS_VERSION"
    restart: always
    volumes:
      - "$PWD/config-tutorial.ini:/opt/dongtai/webapi/conf/config.ini"
  dongtai-web:
    image: "dongtai.docker.scarf.sh/dongtai/dongtai-web:$CHANGE_THIS_VERSION"
    restart: always
    ports:
      - "$WEB_PORT:80"
    volumes:
      - "$PWD/nginx.conf:/etc/nginx/nginx.conf" 
    depends_on:
      - dongtai-webapi
  dongtai-openapi:
    image: "dongtai.docker.scarf.sh/dongtai/dongtai-openapi:$CHANGE_THIS_VERSION"
    restart: always
    volumes:
       - "$PWD/config-tutorial.ini:/opt/dongtai/openapi/conf/config.ini"
  dongtai-engine:
    image: "dongtai.docker.scarf.sh/dongtai/dongtai-engine:$CHANGE_THIS_VERSION"
    restart: always
    volumes:
      - "$PWD/config-tutorial.ini:/opt/dongtai/engine/conf/config.ini"
  dongtai-engine-task:
    image: "dongtai.docker.scarf.sh/dongtai/dongtai-engine:$CHANGE_THIS_VERSION"
    restart: always
    command: ["/opt/dongtai/engine/docker/entrypoint.sh", "task"]
    volumes:
      - "$PWD/config-tutorial.ini:/opt/dongtai/engine/conf/config.ini"
    depends_on:
      - dongtai-engine
EOM

Info "Start to pull new images with tag $TO_VERSION"
docker-compose -p dongtai-iast -f <(echo "$DOCKER_COMPOSE_FILE") pull

Info "Start new containers with tag $TO_VERSION "
docker-compose -p dongtai-iast -f <(echo "$DOCKER_COMPOSE_FILE") up -d

}

function summary()
{
  Notice "-----Upgrade summary start-----"
  Info "Ugrade from $FROM_VERSION to $TO_VERSION. \n"
  Info "Backup file : $backup_filename"
  Info "Executed sql as follow: "
  for SQL in $SQL_NAMES
  do 
    Info $SQL
  done
  Info "Ugrade workdir is $UPGRADE_DIR, this can be delete after upgraded. "
 Notice "-----Upgrade summary end-----"
}

check_param
backup_mysql
check_update_record_file
check_schema_hash
execute_update
check_after_execute
upgrade_docker_image
summary

