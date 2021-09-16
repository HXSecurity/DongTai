#!/bin/bash

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

build_dongtai_iast
