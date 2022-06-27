#!/bin/bash
CURRENT_PATH=$(cd "$(dirname "$0")" || exit;pwd)
SKIP_MYSQL=false
SKIP_REDIS=false
ACCESS_TYPE=ClusterIP
NAMESPACE=dongtai-iast
# latest_version="`wget -qO- -t1 -T2 "https://api.github.com/repos/HXSecurity/DongTai/releases/latest" | jq -r '.tag_name'`"
# REALEASE_VERSION=${latest_version:1}
Info(){
  echo -e "[Info] $1"  2>&1
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
      "n")
        NAMESPACE=$OPTARG
        ;;
      "m")
        ACCESS_TYPE=$OPTARG
        ;;
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
        Info "Usage: ./install.sh -m ClusterIP -s mysql -n dongtai-iast"
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

case "${OUT}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${OUT}"
esac

cd "$CURRENT_PATH" || exit

check_env(){
  if ! [ -x "$(command -v kubectl)" ]; then
    Error "kubectl not installed."
    exit 1
  fi
  context=$(kubectl config current-context)
  Info "Current context: $context"

}

check_permission(){
  Info "Checking kubernetes resources permission ..."
  auths=("secrets" "deployments" "configmaps" "namespaces" "StatefulSet" "Service" )
  for auth in "${auths[@]}";
  do
      out=$(kubectl auth can-i create "$auth")
      if [ "$out" != "yes" ]; then
        Error "No permission to create $auth."
        exit 1
      fi
  done
}

get_latest_image_tag_from_dockerhub() {
  image="$1"
  # Info "start to get latest tag of $image"
  tags=`wget -q https://registry.hub.docker.com/v1/repositories/dongtai/${image}/tags -O -  | sed -e 's/[][]//g' -e 's/"//g' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}'`

  if [ -n "$2" ]
  then
      tags=` echo "${tags}" | grep "$2" `
  fi
  echo "${tags}" | grep -E '^([0-9]+\.){0,2}(\*|[0-9]+)$' | tail -n 1
}


deploy(){
  cd "$CURRENT_PATH" || exit
  ORIG=$1
  FILENAME="$CURRENT_PATH/manifest/$1"
  NEW_FILENAME="$FILENAME.temp"
  NEW_NAMESPACE=$2
  cp "$FILENAME" "$NEW_FILENAME"
  Info "Copying temporary file $NEW_FILENAME ..."

  if [ "${machine}" == "Mac" ]; then
    case $ORIG in
        "2.deploy-redis.yml")
            TAG=$(get_latest_image_tag_from_dockerhub dongtai-redis)
            sed -i "" "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
            sed -i "" "s/CHANGE_THIS_VERSION/$TAG/g" "$NEW_FILENAME" >/dev/null
            ;;
        "3.deploy-mysql.yml")
            MYSQL_TAG=$(get_latest_image_tag_from_dockerhub dongtai-mysql)
            sed -i "" "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
            sed -i "" "s/CHANGE_THIS_VERSION/$MYSQL_TAG/g" "$NEW_FILENAME" >/dev/null
            ;;
        "4.deploy-iast-server.yml")
            WEB_TAG=$(get_latest_image_tag_from_dockerhub dongtai-web)
            SERVER_TAG=$(get_latest_image_tag_from_dockerhub dongtai-server)
            LOGSTASH_TAG=$(get_latest_image_tag_from_dockerhub dongtai-logstash)
            LOGROTATE_TAG=$(get_latest_image_tag_from_dockerhub dongtai-logrotate)
            sed -i "" "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
            sed -i "" "s/dongtai-web:CHANGE_THIS_VERSION/dongtai-web:$WEB_TAG/g" "$NEW_FILENAME" >/dev/null
            sed -i "" "s/dongtai-server:CHANGE_THIS_VERSION/dongtai-server:$SERVER_TAG/g" "$NEW_FILENAME" >/dev/null
            sed -i "" "s/dongtai-logstash:CHANGE_THIS_VERSION/dongtai-server:$LOGSTASH_TAG/g" "$NEW_FILENAME" >/dev/null
            sed -i "" "s/dongtai-logrotate:CHANGE_THIS_VERSION/dongtai-server:$LOGROTATE_TAG/g" "$NEW_FILENAME" >/dev/null
            ;;
        *)
              sed -i "" "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
    esac
  elif [ "${machine}" == "Linux" ]; then
    case $ORIG in
        "2.deploy-redis.yml")
            sed -i  "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
            sed -i  "s/CHANGE_THIS_VERSION/$(get_latest_image_tag_from_dockerhub dongtai-redis)/g" "$NEW_FILENAME" >/dev/null
            ;;
        "3.deploy-mysql.yml")
            sed -i  "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
            sed -i  "s/CHANGE_THIS_VERSION/$(get_latest_image_tag_from_dockerhub dongtai-mysql)/g" "$NEW_FILENAME" >/dev/null
            ;;
        "4.deploy-iast-server.yml")
            WEB_TAG=$(get_latest_image_tag_from_dockerhub dongtai-web)
            SERVER_TAG=$(get_latest_image_tag_from_dockerhub dongtai-server)
            LOGSTASH_TAG=$(get_latest_image_tag_from_dockerhub dongtai-logstash)
            LOGROTATE_TAG=$(get_latest_image_tag_from_dockerhub dongtai-logrotate)
            sed -i "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
            sed -i "s/dongtai-web:CHANGE_THIS_VERSION/dongtai-web:$WEB_TAG/g" "$NEW_FILENAME" >/dev/null
            sed -i "s/dongtai-server:CHANGE_THIS_VERSION/dongtai-server:$SERVER_TAG/g" "$NEW_FILENAME" >/dev/null
            sed -i "" "s/dongtai-logstash:CHANGE_THIS_VERSION/dongtai-server:$LOGSTASH_TAG/g" "$NEW_FILENAME" >/dev/null
            sed -i "" "s/dongtai-logrotate:CHANGE_THIS_VERSION/dongtai-server:$LOGROTATE_TAG/g" "$NEW_FILENAME" >/dev/null
            ;;
        *)
            sed -i  "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
    esac
  else
    Error "Unsupported shell version."
    rm "$NEW_FILENAME"
    exit 1
  fi

  kubectl apply -f "$NEW_FILENAME"

  Info "Cleaning temporary file $NEW_FILENAME ..."
  rm "$NEW_FILENAME"
}

start_deploy(){
  Notice "NAMESPACE: $NAMESPACE, ACCESS_TYPE:$ACCESS_TYPE, SKIP_MYSQL:$SKIP_MYSQL, SKIP_REDIS:$SKIP_REDIS"
  Info "Starting deploy to kubernetes ..."
  deploy "1.create-namespace.yml" "$NAMESPACE"
  if [ $SKIP_REDIS == false ]; then
    deploy "2.deploy-redis.yml" "$NAMESPACE"
  fi
  if [ $SKIP_MYSQL == false ]; then
    deploy "3.deploy-mysql.yml" "$NAMESPACE"
  fi
    deploy "4.deploy-iast-server.yml" "$NAMESPACE"
}
SERVICE_TYPES="NodePort LoadBalancer ClusterIP"
expose_services(){      
    if [[ "$SERVICE_TYPES" =~ "$ACCESS_TYPE" ]]
    then
      kubectl expose deployments/dongtai-web --name=dongtai-web-pub-svc  --port=8000 --target-port=80 -n "$NAMESPACE" --type="$ACCESS_TYPE"
      # kubectl expose deployments/dongtai-openapi --name=dongtai-openapi-pub-svc  --port=8000 --target-port=8000 -n "$NAMESPACE" --type="$ACCESS_TYPE"
    else
      Error "-m option: $SERVICE_TYPES"
    fi
}

check_env
check_permission
start_deploy
expose_services

Info "Installation success!"
Todo "Check services status few minutes later: kubectl get po -n $NAMESPACE"

if [ "$ACCESS_TYPE" == "NodePort" ]; then
    Info "Available node ip:"
    kubectl get nodes -o wide |  awk {'print $7'} | column -t
    Info "dongtai-web service port:] $(kubectl get svc dongtai-web-pub-svc -n "$NAMESPACE" -o=jsonpath='{.spec.ports[0].nodePort}')"
    # Info "dongtai-openapi service port:] $(kubectl get svc dongtai-openapi-pub-svc -n "$NAMESPACE" -o=jsonpath='{.spec.ports[0].nodePort}')"

elif [ "$ACCESS_TYPE" == "LoadBalancer"  ]; then
    Todo "Get EXTERNAL-IP ip or dns by: kubectl get svc dongtai-web-pub-svc -n $NAMESPACE"
else 
  Todo "Your should expose your service [dongtai-web-pub-svc] manually."
fi
