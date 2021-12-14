#!/bin/bash

build_dongtai_iast(){
	echo -e "\n\033[33m[+] install DongTai IAST service, openapi service addr is $1\033[0m"
	chmod u+x deploy/docker-compose/dtctl

	if [ $? -ne 0 ]; then
		./deploy/docker-compose/dtctl install
	else
		./deploy/docker-compose/dtctl install
	fi
	echo -e "\n\033[32m[*] start DongTai IAST service, please wait 30s\033[0m"
}

build_dongtai_iast
