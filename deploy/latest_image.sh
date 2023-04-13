#!/bin/bash
images=("dongtai-server" "dongtai-web" "dongtai-mysql" "dongtai-redis" "dongtai-logrotate" "dongtai-logstash")
for image in ${images[*]}; do
     tags=`curl -s -S "https://registry.hub.docker.com/v2/repositories/dongtai/${image}/tags" | sed -e 's/,/,\n/g' -e 's/\[/\[\n/g' | grep '"name"' | awk -F\" '{print $4;}' | grep -v beta  | sed -n '2p'`
     echo "$image"
     echo "$tags"
     echo -e "\t dongtai/$image:$tags"
     echo -e "\t registry.cn-beijing.aliyuncs.com/huoxian_pub/$image:$tags"
done
