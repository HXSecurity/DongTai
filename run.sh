#!/bin/bash

IP=''
CURRENT_PATH=$(pwd)

build_mysql(){
    cd docker/mysql
    docker build -t huoxian/dongtai-mysql:5.7 .
    docker stop dongtai-mysql || true
    docker rm dongtai-mysql || true
    docker run -d -p 3306:3306 --name dongtai-mysql --restart=always huoxian/dongtai-mysql:5.7
    cd $CURRENT_PATH
}

build_redis(){
    cd docker/redis
    docker build -t huoxian/dongtai-redis:latest .
    docker stop dongtai-redis || true
    docker rm dongtai-redis || true
    docker run -d -p 6379:6379 --name dongtai-redis --restart=always huoxian/dongtai-redis:latest
    cd $CURRENT_PATH
}

build_webapi(){
    cp dongtai-webapi/conf/config.ini.example dongtai-webapi/conf/config.ini

    sed -i "" "s/mysql-server/$1/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/mysql-port/3306/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/database_name/dongtai_webapi/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/mysql_username/root/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/mysql_password/dongtai-iast/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/redis_server/$1/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/redis_port/6379/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/redis_password/123456/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/broker_db/0/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/engine_url/$1:8001/g" dongtai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/api_server_url/$1:8002/g" dongtai-webapi/conf/config.ini >/dev/null

    cd dongtai-webapi
    docker build -t huoxian/dongtai-webapi:latest .
    docker stop dongtai-webapi || true
    docker rm dongtai-webapi || true
    docker run -d -p 8000:8000 --name dongtai-webapi -e debug=true --restart=always huoxian/dongtai-webapi:latest
    cd $CURRENT_PATH
}

build_openapi(){
    cp dongtai-webapi/conf/config.ini dongtai-openapi/conf/config.ini

    cd dongtai-openapi
    docker build -t huoxian/dongtai-openapi:latest .
    docker stop dongtai-openapi || true
    docker rm dongtai-openapi || true
    docker run -d -p 8002:8000 --name dongtai-openapi --restart=always huoxian/dongtai-openapi:latest
    cd $CURRENT_PATH
}

build_engine(){
    cp dongtai-webapi/conf/config.ini dongtai-engine/conf/config.ini

    cd dongtai-engine
    docker build -t huoxian/dongtai-engine:latest .
    docker stop dongtai-engine || true
    docker rm dongtai-engine || true
    docker run -d -p 8001:8000 --name dongtai-engine --restart=always huoxian/dongtai-engine:latest
    cd $CURRENT_PATH
}

build_web(){
    # 修改后端服务的地址
    cp dongtai-web/nginx.conf.example dongtai-web/nginx.conf
    sed -i "" "s/lingzhi-api-svc/$1/g" dongtai-web/nginx.conf >/dev/null

    cd dongtai-web
    # 如果本地有node环境，可自己build部署，否则，直接使用内置的即可
    # npm install
    # npm run build
    docker build -t huoxian/dongtai-web:latest .
    docker stop dongtai-web || true
    docker rm dongtai-web || true
    docker run -d -p 80:80 --name dongtai-web --restart=always huoxian/dongtai-web:latest
    cd $CURRENT_PATH
}

while getopts "i:" arg #选项后面的冒号表示该选项需要参数
do
    case $arg in
        i)
			IP=$OPTARG
            ;;
        ?)  #当有不认识的选项的时候arg为?
            echo "unkonw argument"
            exit 1
        ;;
    esac
done


if [ ! $IP ]; then
    echo "Usage: run.sh -i <ip>, current server ip addr, eg: ./run.sh -i 192.168.2.155"
else
    echo "[+] 开始初始化服务及配置，当前服务器IP：$IP"
    echo -e "\033[33m[+] 开始构建mysql服务...\033[0m"
    #build_mysql
    echo -e "\033[32m[*]\033[0m mysql服务启动成功"

    echo -e "\033[33m[+] 开始构建redis服务...\033[0m"
    #build_redis
    echo -e "\033[32m[*]\033[0m redis服务启动成功"

    echo -e "\033[33m[+] 开始构建dongtai-webapi服务...\033[0m"
    build_webapi $IP
    echo -e "\033[32m[*]\033[0m dongtai-webapi服务启动成功"

    echo -e "\033[33m[+] 开始构建dongtai-openapi服务...\033[0m"
    #build_openapi
    echo -e "\033[32m[*]\033[0m dongtai-openapi服务启动成功"

    echo -e "\033[33m[+] 开始构建dongtai-engine服务...\033[0m"
    #build_engine
    echo -e "\033[32m[*]\033[0m dongtai-engine服务启动成功"

    echo -e "\033[33m[+] 开始构建dongtai-web服务...\033[0m"
    #build_web $IP
    echo -e "\033[32m[*]\033[0m dongtai-web服务启动成功"
fi

