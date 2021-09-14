#!/bin/bash
CURRENT_PATH=$(cd "$(dirname "$0")" || exit;pwd)
SKIP_MYSQL=false
SKIP_REDIS=false
ACCESS_TYPE=NodePort
NAMESPACE=dongtai-iast

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
        Info "Usage: ./install.sh -m NodePort -s mysql -n dongtai-iast"
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

deploy(){
  cd "$CURRENT_PATH" || exit

  FILENAME="$CURRENT_PATH/manifest/$1"
  NEW_FILENAME="$FILENAME.temp"
  NEW_NAMESPACE=$2
  cp "$FILENAME" "$NEW_FILENAME"
  Info "Copying temporary file $NEW_FILENAME ..."
  if [ "${machine}" == "Mac" ]; then
    sed -i "" "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
  elif [ "${machine}" == "Linux" ]; then
    sed -i "s/CHANGE_THIS_NAMESPACE/$NEW_NAMESPACE/g" "$NEW_FILENAME" >/dev/null
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

expose_services(){
  if [ "$ACCESS_TYPE" == "NodePort" ];then
     kubectl expose deployments/dongtai-web --name=dongtai-web-pub-svc  --port=80 --target-port=80 -n "$NAMESPACE" --type=NodePort
     kubectl expose deployments/dongtai-openapi --name=dongtai-openapi-pub-svc  --port=8000 --target-port=8000 -n "$NAMESPACE" --type=NodePort
  elif [ "$ACCESS_TYPE" == "LoadBalancer" ]; then
     kubectl expose deployments/dongtai-web --name=dongtai-web-pub-svc  --port=80 --target-port=80 -n d"$NAMESPACE" --type=LoadBalancer
     kubectl expose deployments/dongtai-openapi --name=dongtai-openapi-pub-svc  --port=8000 --target-port=8000 -n "$NAMESPACE" --type=LoadBalancer
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
    Info "dongtai-openapi service port:] $(kubectl get svc dongtai-openapi-pub-svc -n "$NAMESPACE" -o=jsonpath='{.spec.ports[0].nodePort}')"

elif [ "$ACCESS_TYPE" == "LoadBalancer"  ]; then
    Todo "Get EXTERNAL-IP ip or dns by: kubectl get svc dongtai-web-pub-svc dongtai-openapi-pub-svc -n $NAMESPACE"
fi
