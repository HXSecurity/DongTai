#!/bin/bash
images=("dongtai-server" "dongtai-web" "dongtai-mysql" "dongtai-redis" "dongtai-logrotate" "dongtai-logstash")
for image in ${images[*]}; do
     tags=`wget -q https://registry.hub.docker.com/v1/repositories/dongtai/${image}/tags -O -  | sed -e 's/[][]//g' -e 's/"//g' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}' | grep -E '^([0-9]+\.){0,2}(\*|[0-9]+)$' | tail -n 1 `
     echo "$image"
     echo -e "\t dongtai/$image:$tags"
     echo -e "\t registry.cn-beijing.aliyuncs.com/huoxian_pub/$image:$tags"
done