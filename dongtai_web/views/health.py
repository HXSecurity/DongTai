######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : health
# @created     : Wednesday Aug 25, 2021 12:12:02 CST
#
# @description :
######################################################################


from dongtai_common.endpoint import R
from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import UserEndPoint
from dongtai_web.utils import get_openapi, validate_url
import requests
from urllib.parse import urljoin
from rest_framework.authtoken.models import Token
from requests.exceptions import ConnectionError, ConnectTimeout
import json
import logging
from django.utils.translation import get_language
from dongtai_web.utils import checkopenapistatus

logger = logging.getLogger("dongtai-webapi")

HEALTHPATH = "api/v1/health"


class HealthView(UserEndPoint):
    def get(self, request):
        openapi = get_openapi()
        if openapi is None:
            return R.failure(msg=_("Get OpenAPI configuration failed"))
        if not validate_url(openapi):
            return R.failure(msg=_("OpenAPI service is down, Please check it."))

        token, success = Token.objects.get_or_create(user=request.user)
        openapistatus, openapi_resp = checkopenapistatus(
            urljoin(openapi, HEALTHPATH), token.key
        )
        data = {"dongtai_webapi": 1}
        if openapistatus:
            data.update(openapi_resp)
        else:
            data.update(
                {
                    "dongtai_openapi": {"status": 0},
                    "dongtai_engine": {"status": 0},
                    "oss": {"status": 0},
                    "engine_monitoring_indicators": [],
                }
            )
        cur_language = get_language()
        for indicator in data["engine_monitoring_indicators"]:
            cur_language_field = indicator.get("_".join(["name", cur_language]), None)
            indicator["name"] = (
                cur_language_field if cur_language_field else indicator["name"]
            )
        return R.success(data=data)
