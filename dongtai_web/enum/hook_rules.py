import logging
import json

from django.db.models import Q, F, Count
from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import UserEndPoint, R
from rest_framework.viewsets import ViewSet
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.core.cache import cache
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_common.models.dast_integration import IastDastIntegration
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from dongtai_common.models.profile import IastProfile
from dongtai_conf.settings import DEFAULT_TAINT_VALUE_RANGE_COMMANDS, DEFAULT_IAST_VALUE_TAG

logger = logging.getLogger('dongtai-webapi')


class HookRuleEnumEndPoint(UserEndPoint, viewsets.ViewSet):

    @extend_schema_with_envcheck(summary=_('Hook Rule Enums'),
                                 description=_("Hook Rule Enums "),
                                 tags=[_('Hook Rule')])
    def get_enums(self, request):
        return R.success(
            data={
                "commands": DEFAULT_TAINT_VALUE_RANGE_COMMANDS,
                "tags": DEFAULT_IAST_VALUE_TAG,
            })
