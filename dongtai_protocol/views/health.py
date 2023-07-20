######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : health
# @created     : Wednesday Aug 25, 2021 16:19:13 CST
#
# @description :
######################################################################

import logging
from dongtai_common.endpoint import UserEndPoint, R
from drf_spectacular.utils import extend_schema

from dongtai_protocol.utils import OssDownloader
import oss2
from oss2.exceptions import RequestError
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
import json
from dongtai_protocol.utils import checkossstatus

logger = logging.getLogger("dongtai.openapi")


def checkenginestaus():
    import redis

    mock_data = {
        "dongtai_engine": {"status": 1},
        "engine_monitoring_indicators": [
            {
                "key": "dongtai-replay-vul-scan",
                "value": 0,
                "name": "dongtai-replay-vul-scan",
            },
            {
                "key": "dongtai_method_pool_scan",
                "value": 0,
                "name": "dongtai-method-pool-scan",
            },
        ],
    }
    # 读取数据库中的redis键,然后查找队列大小
    from dongtai_common.models.engine_monitoring_indicators import (
        IastEnginMonitoringIndicators,
    )

    try:
        monitor_models = IastEnginMonitoringIndicators.objects.all()
        if monitor_models.values("id").count() > 0:
            from dongtai_conf import settings

            redis_cli = redis.StrictRedis(
                host=settings.config.get("redis", "host"),
                password=settings.config.get("redis", "password"),
                port=settings.config.get("redis", "port"),
                db=settings.config.get("redis", "db"),
            )

            monitor_models = monitor_models.values("key", "name", "name_en", "name_zh")
            mock_data["engine_monitoring_indicators"] = []
            for monitor_model in monitor_models:
                mock_data["engine_monitoring_indicators"].append(
                    {
                        "key": monitor_model["key"],
                        "name": monitor_model["name"],
                        "name_en": monitor_model["name_en"],
                        "name_zh": monitor_model["name_zh"],
                        "value": redis_cli.llen(monitor_model["key"]),
                    }
                )
    except Exception as e:
        logger.info(e)
        return R.success(data=mock_data)
    return R.success(data=mock_data)


def _checkenginestatus():
    try:
        resp = checkenginestaus()
        resp = json.loads(resp.content)
        resp = resp.get("data", None)
    except (ConnectionError, ConnectTimeout):
        return False, None
    except Exception as e:
        logger.info(f"HealthView_checkenginestatus:{e}")
        return False, None
    return True, resp


class HealthView(UserEndPoint):
    @extend_schema(
        description="Check OpenAPI Service Status",
        responses=R,
        methods=["GET"],
        summary="检查 OpenAPI 服务状态",
        tags=["OpenAPI"],
    )
    def get(self, request):
        oss_status, _ = checkossstatus()
        statusmap = {True: 1, False: 0}
        engine_status, engine_resp = _checkenginestatus()
        data = {
            "dongtai_openapi": {"status": 1},
            "oss": {"status": statusmap[oss_status]},
        }
        if engine_status and engine_resp is not None:
            data.update(engine_resp)
        else:
            data.update({"dongtai_engine": 0, "engine_monitoring_indicators": []})
        return R.success(data=data)
