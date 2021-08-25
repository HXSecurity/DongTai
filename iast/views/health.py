######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : health
# @created     : Wednesday Aug 25, 2021 12:12:02 CST
#
# @description :
######################################################################



from dongtai.endpoint import R
from django.utils.translation import gettext_lazy as _
from dongtai.endpoint import UserEndPoint
from iast.utils import get_openapi, validate_url
import requests
from urllib.parse import urljoin
from rest_framework.authtoken.models import Token
from requests.exceptions import ConnectionError, ConnectTimeout
import json
import logging
logger = logging.getLogger('dongtai-webapi')

HEALTHPATH = 'api/v1/path'


class HealthView(UserEndPoint):
    def get(self, request):
        openapi = get_openapi()
        if openapi is None:
            return R.failure(msg=_("Get OpenAPI configuration failed"))
        if not validate_url(openapi):
            return R.failure(msg=_("OpenAPI configuration error"))

        token, success = Token.objects.get_or_create(user=request.user)
        openapistatus, openapi_resp = _checkopenapistatus(
            urljoin(openapi, HEALTHPATH), token.key)
        data = {"dongtai_webapi": 1}
        if openapistatus:
            data.update(openapi_resp)
        else:
            data.update({
                "dongtai_openapi": {
                    "status": 0
                },
                "dongtai_engine": {
                    "status": 0
                },
                "oss": {
                    "status": 0
                },
                "engine_monitoring_indicators": [],
            })
        return R.success(data=data)


def _checkopenapistatus(openapiurl, token):
    try:
        resp = requests.get(
            openapiurl,
            timeout=5,
            headers={'Authorization': "Token {}".format(token)})
        resp = json.load(resp.content)
        resp = resp.get("data", None)
    except (ConnectionError, ConnectTimeout):
        return False, None
    except Exception as e:
        logger.log("HealthView_checkenginestatus:{}".format(e))
        return False, None
    return True, resp
