# download source code

# Check if the Docker service is turned on
check_docker(){
	echo "\n\033[33m[+] check docker servie status\033[0m"
	docker ps 1>/dev/null 2>/dev/null
	
	if [ $? -ne 0 ]; then
		echo "\033[31m[-] docker service is down. please start docker service and rerun.\033[0m"
		exit
	else
		echo "\033[32m[*]\033[0m docker service is up."
	fi
}

# Specify the port of Web, OpenAPI service and check whether it is available
check_port(){
	echo "\n\033[33m[+] check port status\033[0m"

	read -p "[+] please input web service port, default [80]:" WEB_SERVICE_PORT
	if [ -z $WEB_SERVICE_PORT ];then
		WEB_SERVICE_PORT=80
	fi

	lsof -i:$WEB_SERVICE_PORT|grep "LISTEN" 2>/dev/null
	
	if [ $? -ne 0 ]; then
		echo "\033[32m[*]\033[0m port $WEB_SERVICE_PORT is ok."
	else
		echo "\033[31m[-] port $WEB_SERVICE_PORT is already in use. please change default port\033[0m"
		exit
	fi

	read -p "[+] please input openAPI service port, default [8000]:" OPENAPI_SERVICE_PORT
	if [ -z $OPENAPI_SERVICE_PORT ];then
		OPENAPI_SERVICE_PORT=8000
	fi
	lsof -i:$OPENAPI_SERVICE_PORT | grep "LISTEN" 2>/dev/null

	if [ $? -ne 0 ]; then
		echo "\033[32m[*]\033[0m port $OPENAPI_SERVICE_PORT is ok."
	else
		echo "\033[31m[-] port $OPENAPI_SERVICE_PORT is already in use. please change default port\033[0m"
		exit
	fi

	echo '''version: "2"
services:
  dongtai-mysql:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-mysql:latest
    restart: always
    volumes:
      - ./data:/var/lib/mysql:rw

  dongtai-redis:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-redis:latest
    restart: always

  dongtai-webapi:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-webapi:latest
    restart: always
    volumes:
      - $PWD/config-tutorial.ini:/opt/dongtai/webapi/conf/config.ini
    depends_on:
      - dongtai-mysql
      - dongtai-redis

  dongtai-web:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-web:latest
    restart: always
    ports:
      - "'''$WEB_SERVICE_PORT''':80"
    volumes:
      - $PWD/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - dongtai-webapi

  dongtai-openapi:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-openapi:latest
    restart: always
    volumes:
       - $PWD/config-tutorial.ini:/opt/dongtai/openapi/conf/config.ini
    ports:
      - "'''$OPENAPI_SERVICE_PORT''':8000"
    depends_on:
      - dongtai-mysql
      - dongtai-redis

  dongtai-engine:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-engine:latest
    restart: always
    volumes:
      - $PWD/config-tutorial.ini:/opt/dongtai/engine/conf/config.ini
    depends_on:
      - dongtai-mysql
      - dongtai-redis

  dongtai-engine-task:
    image: registry.cn-beijing.aliyuncs.com/huoxian_pub/dongtai-engine:latest
    restart: always
    command: ["/opt/dongtai/engine/docker/entrypoint.sh", "task"]
    volumes:
      - $PWD/config-tutorial.ini:/opt/dongtai/engine/conf/config.ini
    depends_on:
      - dongtai-mysql
      - dongtai-redis
      - dongtai-engine''' > deploy/docker-compose/docker-compose.yml
}

build_dongtai_iast(){
	echo "\n\033[33m[+] install DongTai IAST service, openapi service addr is $1\033[0m"
	chmod u+x deploy/docker-compose/install.sh
	if [ $? -ne 0 ]; then
		bash deploy/docker-compose/install.sh $1
	else
		./deploy/docker-compose/install.sh $1
	fi
	echo "\n\033[32m[*] start DongTai IAST service, please wait 30s\033[0m"
}

check_docker
check_port
build_dongtai_iast
