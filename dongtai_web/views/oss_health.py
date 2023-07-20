######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : oss_health
# @created     : Thursday Aug 26, 2021 10:51:06 CST
#
# @description :
######################################################################
from dongtai_web.utils import get_openapi, validate_url
from urllib.parse import urljoin
from rest_framework.authtoken.models import Token
from dongtai_web.utils import checkopenapistatus
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.endpoint import R
from django.utils.translation import gettext_lazy as _

OSSHEALTHPATH = "api/v1/oss/health"


class OssHealthView(UserEndPoint):
    def get(self, request):
        openapi = get_openapi()
        if openapi is None:
            return R.failure(msg=_("Get OpenAPI configuration failed"))
        if not validate_url(openapi):
            return R.failure(msg=_("OpenAPI configuration error"))

        token, success = Token.objects.get_or_create(user=request.user)
        openapistatus, openapi_resp = checkopenapistatus(
            urljoin(openapi, OSSHEALTHPATH), token.key
        )
        if openapistatus:
            return R.success(data=openapi_resp)
        return R.success(data={"oss": {"status": 0}})
