#!/bin/bash
set -x
build_dongtai_iast(){
	echo -e "Start to install DongTai IAST service"
	chmod u+x deploy/docker-compose/dtctl
	cd deploy/docker-compose/
	./dtctl install
}

build_dongtai_iast
