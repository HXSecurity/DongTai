#!/usr/bin/env python
# datetime:2020/8/12 15:08

import logging

from django.http import StreamingHttpResponse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token

from dongtai_common.endpoint import OpenApiEndPoint

logger = logging.getLogger("django")

TEMPLAGE_DATA = """#/bin/bash
PID=''
URL='{url}'
TOKEN='{token}'

banner(){
    echo "\n\t\tLingZhi IAST\n\n"
}

mkpath(){
    rm -rf ~/.iast
    mkdir ~/.iast
}

# download lingzhi agent.jar
download(){
    curl -X GET $1/api/v1/agent/download?url=$1 -H "Authorization: Token $2" -o ~/.iast/agent.jar -k
}

# attach agent.jar to pid
run(){
    if [ -n "$1" ];then
        echo "[+] 检测引擎开始安装,进程ID:$1"
        java -jar ~/.iast/agent.jar -m install -p $1
        echo "[-] 检测引擎安装完成,进程ID:$1"
    fi
}

choice_pid(){
    ajps=($(ps -ef|grep java |grep -v grep|awk '{print $2}'))
    len=${#ajps[@]}

    if [ 0 -ne $len ]; then
        mkpath
        download $URL $TOKEN

        for ((i=0; i<${len};i+=1));
        do
            run ${ajps[i]}
        done

    else
        echo '未发现任何Java进程,终止安装进程'
        exit
    fi
}

while getopts "u:" arg #选项后面的冒号表示该选项需要参数
do
     case $arg in
        u)
            URL=$OPTARG
            ;;
        ?)  #当有不认识的选项的时候arg为?
            echo "unkonw argument"
            exit 1
        ;;
    esac
done

if [ ! $URL ]; then
    echo "Usage: lingzhi.sh -u <url>\n\t-u <url>, iast server url, eg: http://127.0.0.1:8000"
else
    # 检查并选择需要attach的进程
    banner
    choice_pid
fi
"""


class AutoDeployEndPoint(OpenApiEndPoint):
    """
    当前用户详情
    """

    name = "download_iast_agent"
    description = "白帽子-下载IAST 自动部署脚本"

    @extend_schema(
        summary="下载 IAST 自动部署脚本",
        tags=["Agent"],
        deprecated=True,
    )
    def get(self, request):
        """
        IAST下载 agent接口
        :param request:
        :return:
        """
        try:
            url = request.query_params["url"]
            token, success = Token.objects.get_or_create(user=request.user)
            data = TEMPLAGE_DATA.replace("{url}", url).replace("{token}", token.key)
            return StreamingHttpResponse(data)
        except Exception as e:
            logger.info(e)
            return StreamingHttpResponse(TEMPLAGE_DATA)
