#!/bin/bash

CURRENT_PATH=$(pwd)

create_network(){
    docker network rm dongtai-net || true
    docker network create dongtai-net
}

build_mysql(){
    cd docker/mysql
    docker build -t huoxian/dongtai-mysql:5.7 .
    docker stop dongtai-mysql || true
    docker rm dongtai-mysql || true
    docker run -d --network dongtai-net --name dongtai-mysql --restart=always huoxian/dongtai-mysql:5.7
    cd $CURRENT_PATH
}

build_redis(){
    cd docker/redis
    docker build -t huoxian/dongtai-redis:latest .
    docker stop dongtai-redis || true
    docker rm dongtai-redis || true
    docker run -d --network dongtai-net --name dongtai-redis --restart=always huoxian/dongtai-redis:latest
    cd $CURRENT_PATH
}

build_webapi(){
    cp DongTai-webapi/conf/config.ini.example DongTai-webapi/conf/config.ini

    sed -i "" "s/mysql-server/dongtai-mysql/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/mysql-port/3306/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/database_name/dongtai_webapi/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/mysql_username/root/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/mysql_password/dongtai-iast/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/redis_server/dongtai-redis/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/redis_port/6379/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/redis_password/123456/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/broker_db/0/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/engine_url/dongtai-engine:8000/g" DongTai-webapi/conf/config.ini >/dev/null
    sed -i "" "s/api_server_url/dongtai-openapi:8000/g" DongTai-webapi/conf/config.ini >/dev/null

    cd DongTai-webapi
    docker build -t huoxian/dongtai-webapi:latest .
    docker stop dongtai-webapi || true
    docker rm dongtai-webapi || true
    docker run -d --network dongtai-net --name dongtai-webapi -e debug=true --restart=always huoxian/dongtai-webapi:latest
    cd $CURRENT_PATH
}

build_openapi(){
    cp DongTai-webapi/conf/config.ini DongTai-openapi/conf/config.ini

    cd DongTai-openapi
    docker build -t huoxian/dongtai-openapi:latest .
    docker stop dongtai-openapi || true
    docker rm dongtai-openapi || true
    docker run -d --network dongtai-net --name dongtai-openapi --restart=always huoxian/dongtai-openapi:latest
    cd $CURRENT_PATH
}

build_engine(){
    cp DongTai-webapi/conf/config.ini DongTai-engine/conf/config.ini

    cd DongTai-engine
    docker build -t huoxian/dongtai-engine:latest .
    docker stop dongtai-engine || true
    docker rm dongtai-engine || true
    docker run -d --network dongtai-net --name dongtai-engine --restart=always huoxian/dongtai-engine:latest
    cd $CURRENT_PATH
}

build_web(){
    # 修改后端服务的地址
    cp DongTai-web/nginx.conf.example DongTai-web/nginx.conf
    sed -i "" "s/lingzhi-api-svc/dongtai-webapi/g" DongTai-web/nginx.conf >/dev/null

    cd DongTai-web
    # 如果本地有node环境，可自己build部署，否则，直接使用内置的即可
    # npm install
    # npm run build
    docker build -t huoxian/dongtai-web:latest .
    docker stop dongtai-web || true
    docker rm dongtai-web || true
    docker run -d -p 80:80 --network dongtai-net --name dongtai-web --restart=always huoxian/dongtai-web:latest
    cd $CURRENT_PATH
}

download_source_code(){
    git submodule init
    git submodule update
}


echo "[+] 开始初始化服务及配置"

echo -e "\033[33m[+] 开始下载代码...\033[0m"
# download_source_code
echo -e "\033[32m[*]\033[0m 代码下载成功，准备构建"

echo -e "\033[33m[+] 开始创建虚拟网络...\033[0m"
# create_network
echo -e "\033[32m[*]\033[0m 虚拟网络创建成功"

echo -e "\033[33m[+] 开始构建mysql服务...\033[0m"
build_mysql
echo -e "\033[32m[*]\033[0m mysql服务启动成功"

echo -e "\033[33m[+] 开始构建redis服务...\033[0m"
# build_redis
echo -e "\033[32m[*]\033[0m redis服务启动成功"

echo -e "\033[33m[+] 开始构建DongTai-webapi服务...\033[0m"
# build_webapi
echo -e "\033[32m[*]\033[0m DongTai-webapi服务启动成功"

echo -e "\033[33m[+] 开始构建DongTai-openapi服务...\033[0m"
# build_openapi
echo -e "\033[32m[*]\033[0m DongTai-openapi服务启动成功"

echo -e "\033[33m[+] 开始构建DongTai-engine服务...\033[0m"
# build_engine
echo -e "\033[32m[*]\033[0m DongTai-engine服务启动成功"

echo -e "\033[33m[+] 开始构建DongTai-web服务...\033[0m"
# build_web
echo -e "\033[32m[*]\033[0m DongTai-web服务启动成功"
