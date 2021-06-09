#!/bin/bash
CURRENT_PATH=$(cd "$(dirname "$0")" || exit;pwd)
SKIP_MYSQL=false
SKIP_REDIS=false
ACCESS_TYPE=NodePort

while getopts ":m:s:h" optname
do
    case "$optname" in
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
        echo "Usage: ./install.sh -m NodePort -s mysql"
        exit 1
        ;;
      ":")
        echo "No argument value for option $OPTARG"
        ;;
      "?")
        echo "Unknown option $OPTARG"
        ;;
      *)
        echo "Unknown error while processing options"
        ;;
    esac
done


cd "$CURRENT_PATH" || exit

check_env(){
  if ! [ -x "$(command -v kubectl)" ]; then
    echo '[Error] kubectl not installed.'
    exit 1
  fi
  context=$(kubectl config current-context)
  echo "[Info] Current context: $context"

}

check_permission(){
  echo "[Info] Checking kubernetes resources permission ..."
  auths=("secrets" "deployments" "configmaps" "namespaces" "StatefulSet" "Service" )
  for auth in "${auths[@]}";
  do
      out=$(kubectl auth can-i create "$auth")
      if [ "$out" != "yes" ]; then
        echo "[Error] No permission to create $auth."
        exit 1
      fi
  done
}

start_deploy(){
  echo "[Info] ACCESS_TYPE:$ACCESS_TYPE, SKIP_MYSQL:$SKIP_MYSQL,SKIP_REDIS:$SKIP_REDIS"
  echo "[Info] Starting deploy to kubernetes ..."
  kubectl apply -f "$CURRENT_PATH/manifest/1.create-namespace.yml"
  if [ $SKIP_REDIS == false ]; then
    kubectl apply -f "$CURRENT_PATH/manifest/2.deploy-redis.yml"
  fi
  if [ $SKIP_MYSQL == false ]; then
    kubectl apply -f "$CURRENT_PATH/manifest/3.deploy-mysql.yml"
  fi
  kubectl apply -f "$CURRENT_PATH/manifest/4.deploy-iast-server.yml"
}

expose_services(){
  if [ "$ACCESS_TYPE" == "NodePort" ];then
     kubectl expose deployments/dongtai-web --name=dongtai-web-pub-svc  --port=80 --target-port=80 -n dongtai-iast --type=NodePort
     kubectl expose deployments/dongtai-engine --name=dongtai-engine-pub-svc  --port=8000 --target-port=8000 -n dongtai-iast --type=NodePort
  elif [ "$ACCESS_TYPE" == "LoadBalancer" ]; then
     kubectl expose deployments/dongtai-web --name=dongtai-web-pub-svc  --port=80 --target-port=80 -n dongtai-iast --type=LoadBalancer
     kubectl expose deployments/dongtai-engine --name=dongtai-engine-pub-svc  --port=8000 --target-port=8000 -n dongtai-iast --type=LoadBalancer
  fi
}

check_env
check_permission
start_deploy
expose_services

echo "[Info] Installation success!"

echo "[Todo] Check services status few minutes later: kubectl get po -n dongtai-iast"

if [ "$ACCESS_TYPE" == "NodePort" ]; then
    echo "[Info] Available node ip:"
    kubectl get nodes -o wide |  awk {'print $7'} | column -t
    echo "[Info] dongtai-web service port:] $(kubectl get svc dongtai-web-pub-svc -n dongtai-iast -o=jsonpath='{.spec.ports[0].nodePort}')"
    echo "[Info] dongtai-engine service port:] $(kubectl get svc dongtai-engine-pub-svc -n dongtai-iast -o=jsonpath='{.spec.ports[0].nodePort}')"

elif [ "$ACCESS_TYPE" == "LoadBalancer"  ]; then
    echo "[Todo] Get EXTERNAL-IP ip or dns by: kubectl get svc dongtai-web-pub-svc dongtai-engine-pub-svc -n dongtai-iast"
fi
