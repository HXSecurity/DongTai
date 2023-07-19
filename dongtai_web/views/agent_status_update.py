#!/usr/bin/env python
import time

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_common.utils import const
from dongtai_common.utils.const import OPERATE_PUT
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(((201, _("Engine status was updated successfully.")), ""),)
)


class AgentStatusUpdate(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Agent"), OPERATE_PUT],
        summary="探针状态修改",
        deprecated=True,
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        timestamp = int(time.time())
        queryset = IastAgent.objects.filter(user=request.user)
        no_heart_beat_queryset = queryset.filter(
            (Q(server=None) & Q(latest_time__lt=(timestamp - 600))),
            online=const.RUNNING,
        )
        no_heart_beat_queryset.update(online=0)

        heart_beat_queryset = queryset.filter(
            server__update_time__lt=(timestamp - 600), online=const.RUNNING
        )
        heart_beat_queryset.update(online=0)

        return R.success(msg=_("Engine status was updated successfully."))
