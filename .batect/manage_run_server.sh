#!/usr/bin/env sh

######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : manage_run_server
# @created     : 星期二 1月 25, 2022 10:39:21 CST
#
# @description : 
######################################################################

if [ "$PYTHONAGENT" = "TRUE" ]; then
	curl -X GET "${DONGTAI_IAST_BASE_URL}/api/v1/agent/download?url=${DONGTAI_IAST_BASE_URL}&language=python&projectName=${PROJECT_NAME}" -H "Authorization: Token ${DONGTAI_AGNET_TOKEN}" -o dongtai-agent-python.tar.gz -k
	pip install dongtai-agent-python.tar.gz
fi
python manage.py runserver 0.0.0.0:8000
