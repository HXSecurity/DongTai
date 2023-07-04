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
import logging
from dongtai_protocol.utils import checkossstatus, STATUSMAP
from dongtai_common.endpoint import OpenApiEndPoint, R, UserEndPoint

logger = logging.getLogger("dongtai.openapi")


class OSSHealthView(UserEndPoint):
    @extend_schema(
        description='Check OSS Health',
        responses=R,
        methods=['GET'],
        summary="Check OSS Health",
        tags=["OSS"],
    )
    def get(self, request):
        oss_status, _ = checkossstatus()
        data = {"oss": {"status": 1}}
        # data = {"oss": {"status": STATUSMAP[oss_status]}}
        return R.success(data=data)
