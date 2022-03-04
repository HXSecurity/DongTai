######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : engine_method_pool_time_range
# @created     : 星期四 10月 21, 2021 17:57:16 CST
#
# @description :
######################################################################



from functools import reduce

from django.db.models import Q
from dongtai.endpoint import R, AnonymousAndUserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.project import IastProject
from dongtai.models.user import User
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.hook_type import HookType

from iast.utils import get_model_field, assemble_query
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy
from django.db.utils import OperationalError
import re
import operator
import time
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy

_GetResponseSerializer = get_response_serializer(
    serializers.IntegerField(help_text=_('the eariest time of method_pool')))


class MethodPoolTimeRangeProxy(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck(tags=[_('Method Pool')],
                                 summary=_('Method Pool Time Range'),
                                 description=_("get method_pool eariest time"),
                                 response_schema=_GetResponseSerializer)
    def get(self, request):
        q = Q(agent_id__in=[
            item['id'] for item in list(
                self.get_auth_agents_with_user(request.user).values('id'))
        ])
        mintime = MethodPool.objects.filter(q).values_list(
            'update_time').order_by('-update_time').first()
        if mintime is None:
            return R.failure()
        return R.success(data=mintime)
