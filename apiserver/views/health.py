######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : health
# @created     : Wednesday Aug 25, 2021 16:19:13 CST
#
# @description :
######################################################################

import logging
from dongtai.endpoint import OpenApiEndPoint, R
from apiserver.utils import OssDownloader
from AgentServer import settings
import oss2
from oss2.exceptions import RequestError
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
import json

logger = logging.getLogger("dongtai.openapi")


def _checkossstatus():
    try:
        auth = oss2.Auth(settings.ACCESS_KEY, settings.ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth,
                             settings.BUCKET_URL,
                             settings.BUCKET_NAME,
                             connect_timeout=2)
        bucket.list_objects()
    except RequestError:
        return False, None
    except Exception as e:
        logger.info("HealthView_checkossstatus:{}".format(e))
        return False, None
    return True, None


def _checkenginestatus():
    try:
        resp = requests.get(settings.HEALTH_ENGINE_URL, timeout=1)
        resp = json.load(resp.content)
        resp = resp.get("data", None)
    except (ConnectionError, ConnectTimeout):
        return False, None
    except Exception as e:
        logger.info("HealthView_checkenginestatus:{}".format(e))
        return False, None
    return True, resp


class HealthView(OpenApiEndPoint):
    def get(self, request):
        oss_status, _ = _checkossstatus()
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
