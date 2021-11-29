#!/bin/bash

build_dongtai_iast(){
	echo -e "\n\033[33m[+] install DongTai IAST service, openapi service addr is $1\033[0m"
	chmod u+x deploy/docker-compose/dtctl

	latest_version="`wget -qO- -t1 -T2 "https://api.github.com/repos/HXSecurity/DongTai/releases/latest" | jq -r '.tag_name'`"
	latest_version=${latest_version:1}
	echo  "Install version is $latest_version"

	if [ $? -ne 0 ]; then
		./deploy/docker-compose/dtctl install -v $latest_version
	else
		./deploy/docker-compose/dtctl install -v $latest_version
	fi
	echo -e "\n\033[32m[*] start DongTai IAST service, please wait 30s\033[0m"
}

build_dongtai_iast
