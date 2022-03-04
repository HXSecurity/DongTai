######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : health
# @created     : Wednesday Aug 25, 2021 16:19:13 CST
#
# @description :
######################################################################

import logging
from dongtai.endpoint import OpenApiEndPoint, R
from drf_spectacular.utils import extend_schema

from apiserver.utils import OssDownloader
from AgentServer import settings
import oss2
from oss2.exceptions import RequestError
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
import json
from apiserver.utils import checkossstatus

logger = logging.getLogger("dongtai.openapi")


def _checkenginestatus():
    try:
        resp = requests.get(settings.HEALTH_ENGINE_URL, timeout=4)
        resp = json.loads(resp.content)
        resp = resp.get("data", None)
    except (ConnectionError, ConnectTimeout):
        return False, None
    except Exception as e:
        logger.info("HealthView_checkenginestatus:{}".format(e))
        return False, None
    return True, resp


class HealthView(OpenApiEndPoint):
    @extend_schema(
        description='Check OpenAPI Service Status',
        responses=R,
        methods=['GET']
    )
    def get(self, request):
        oss_status, _ = checkossstatus()
        statusmap = {True: 1, False: 0}
        engine_status, engine_resp = _checkenginestatus()
        data = {
            "dongtai_openapi": {
                "status": 1
            },
            "oss": {
                "status": statusmap[oss_status]
            }
        }
        if engine_status:
            data.update(engine_resp)
        else:
            data.update({
                "dongtai_engine": 0,
                "engine_monitoring_indicators": []
            })
        return R.success(data=data)
