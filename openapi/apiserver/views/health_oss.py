######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : health_oss
# @created     : Thursday Aug 26, 2021 10:37:17 CST
#
# @description :
######################################################################

import oss2
from drf_spectacular.utils import extend_schema
from oss2.exceptions import RequestError
from AgentServer import settings
import logging
from apiserver.utils import checkossstatus, STATUSMAP
from dongtai.endpoint import OpenApiEndPoint, R

logger = logging.getLogger("dongtai.openapi")


class OSSHealthView(OpenApiEndPoint):
    @extend_schema(
        description='Check OSS Health',
        responses=R,
        methods=['GET']
    )
    def get(self, request):
        oss_status, _ = checkossstatus()
        data = {"oss": {"status": STATUSMAP[oss_status]}}
        return R.success(data=data)
