#!/bin/bash
VERSION='1.0.0'
CURRENT_PATH=$(pwd)
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

download_dongati(){
    read -p "[+] please input DongTai Version, default [1.0.0]:" VERSION
    if [ -z $VERSION ];then
        VERSION='1.0.0'
    fi

    read -p "[+] if you need download DongTai images package, please input download url, default:[N]:" DOWNLOAD_URL
    if [ "" != "$DOWNLOAD_URL" ];then
        curl $DOWNLOAD_URL -o "dongtai-iast-$VERSION.tar.gz"
    fi
    
    if [ ! -f "dongtai-iast-$VERSION.tar.gz" ];then
        echo "dongtai-iast-$VERSION.tar.gz is not exist."
        exit
    else
        tar -zxvf "dongtai-iast-$VERSION.tar.gz"
    fi
}

import_offical_image(){
    cd "$CURRENT_PATH/dongtai-iast-$VERSION"

    echo -e "\033[33m[+] import dongtai-openapi-$VERSION...\033[0m"
    if [ ! -f "dongtai-openapi-$VERSION.tar" ];then
        echo 'DongTai-OpenAPI Images is not exist.'
    else
        cat dongtai-openapi-$VERSION.tar | docker import --change "CMD [\"/usr/local/bin/uwsgi\",\"--ini\", \"/opt/dongtai/openapi/conf/uwsgi.ini\"]"  - registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-openapi:$VERSION
    fi

    echo -e "\033[33m[+] import dongtai-mysql-$VERSION...\033[0m"
    if [ ! -f "dongtai-mysql-$VERSION.tar" ];then
        echo 'DongTai-MySql Images is not exist.'
    else
        docker load < dongtai-mysql-$VERSION.tar
    fi

    echo -e "\033[33m[+] import dongtai-redis-$VERSION...\033[0m"
    if [ ! -f "dongtai-redis-$VERSION.tar" ];then
        echo 'DongTai-Redis Images is not exist.'
    else
        docker load < dongtai-redis-$VERSION.tar
    fi

    echo -e "\033[33m[+] import dongtai-engine-$VERSION...\033[0m"
    if [ ! -f "dongtai-engine-$VERSION.tar" ];then
        echo 'DongTai-Engine Images is not exist.'
    else
        docker load < dongtai-engine-$VERSION.tar
    fi

    echo -e "\033[33m[+] import dongtai-web-$VERSION...\033[0m"
    if [ ! -f "dongtai-web-$VERSION.tar" ];then
        echo 'DongTai-Web Images is not exist.'
    else
        docker load < dongtai-web-$VERSION.tar
    fi

    echo -e "\033[33m[+] import dongtai-webapi-$VERSION...\033[0m"
    if [ ! -f "dongtai-webapi-$VERSION.tar" ];then
        echo 'DongTai-WebAPI Images is not exist.'
    else
        docker load < dongtai-webapi-$VERSION.tar
    fi
}

create_network(){
    docker network rm dongtai-net || true
    docker network create dongtai-net
}

run_mysql(){
    docker stop dongtai-mysql || true
    docker rm dongtai-mysql || true
    docker run -d --network dongtai-net --name dongtai-mysql --restart=always registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:1.0.0
}

run_redis(){
    docker stop dongtai-redis || true
    docker rm dongtai-redis || true
    docker run -d --network dongtai-net --name dongtai-redis --restart=always registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-redis:1.0.0
}

run_webapi(){
    docker stop dongtai-webapi || true
    docker rm dongtai-webapi || true
    docker run -d --network dongtai-net --name dongtai-webapi -e debug=false --restart=always registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-webapi:1.0.0
}

run_openapi(){
    docker stop dongtai-openapi || true
    docker rm dongtai-openapi || true
    docker run -d --network dongtai-net -p $1:8000 --name dongtai-openapi --restart=always registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-openapi:1.0.0
}

run_engine(){
    docker stop dongtai-engine || true
    docker rm dongtai-engine || true
    docker run -d --network dongtai-net --name dongtai-engine --restart=always registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-engine:1.0.0
}

run_engine_task(){
    docker stop dongtai-engine-task || true
    docker rm dongtai-engine-task || true
    docker run -d --network dongtai-net --name dongtai-engine-task --restart=always registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-engine:1.0.0 bash /opt/dongtai/engine/docker/entrypoint.sh task
}

run_web(){
    docker stop dongtai-web || true
    docker rm dongtai-web || true
    docker run -d -p $1:80 --network dongtai-net --name dongtai-web --restart=always registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-web:1.0.0
    cd $CURRENT_PATH
}

echo "[+] Current System: ${machine}, initlialing..."
echo -e "\033[33m[+] Download DongTai Images...\033[0m"
download_dongati
echo -e "\033[32m[*]\033[0m done."

echo -e "\033[33m[+] Import DongTai Images...\033[0m"
import_offical_image
echo -e "\033[32m[*]\033[0m done."

echo -e "\033[33m[+] Create Docker Network: dongtai-net\033[0m"
create_network
echo -e "\033[32m[*]\033[0m done."

echo -e "\033[33m[+] start mysql service...\033[0m"
run_mysql
echo -e "\033[32m[*]\033[0m done."

echo -e "\033[33m[+] start redis service...\033[0m"
run_redis
echo -e "\033[32m[*]\033[0m done."

echo -e "\033[33m[+] start dongtai-webapi service...\033[0m"
run_webapi
echo -e "\033[32m[*]\033[0m done."

echo -e "\033[33m[+] start dongtai-openapi service...\033[0m"
run_openapi
echo -e "\033[32m[*]\033[0m done."

echo -e "\033[33m[+] start dongtai-engine service...\033[0m"
run_engine
echo -e "\033[32m[*]\033[0m done."

echo -e "\033[33m[+] start dongtai-engine-task service...\033[0m"
run_engine_task
echo -e "\033[32m[*]\033[0m done."

echo -e "\033[33m[+] start dongtai-web service...\033[0m"
run_web
echo -e "\033[32m[*]\033[0m done."
