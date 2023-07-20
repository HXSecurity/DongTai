import logging

from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import UserEndPoint, R
from dongtai_web.utils import extend_schema_with_envcheck
from rest_framework import viewsets
from dongtai_conf.settings import (
    DEFAULT_TAINT_VALUE_RANGE_COMMANDS,
    DEFAULT_IAST_VALUE_TAG,
)

logger = logging.getLogger("dongtai-webapi")


class HookRuleEnumEndPoint(UserEndPoint, viewsets.ViewSet):
    @extend_schema_with_envcheck(
        summary=_("Hook Rule 枚举"),
        description=_("Hook Rule Enums "),
        tags=[_("Hook Rule")],
    )
    def get_enums(self, request):
        return R.success(
            data={
                "commands": DEFAULT_TAINT_VALUE_RANGE_COMMANDS,
                "tags": DEFAULT_IAST_VALUE_TAG,
            }
        )
