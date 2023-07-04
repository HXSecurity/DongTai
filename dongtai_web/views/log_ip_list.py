import logging

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.log import IastLog
from dongtai_common.models.user import User

logger = logging.getLogger("dongtai-webapi")


class LogsIPList(UserEndPoint):
    name = "api-v2-logs-ip-list"
    description = _("Log list")

    @extend_schema(
        description="Get list of logs ip.",
        summary="Log IP List",
        tags=["Logs"],
    )
    def get(self, request: Request) -> JsonResponse:
        user: User = request.user  # type: ignore

        try:
            if user.is_system_admin():
                queryset = IastLog.objects.all()
            elif user.is_talent_admin():
                users = self.get_auth_users(user)
                user_ids = list(users.values_list("id", flat=True))
                queryset = IastLog.objects.filter(user_id__in=user_ids)
            else:
                queryset = IastLog.objects.filter(user=user)

            data = list(
                queryset.values_list("access_ip", flat=True)
                .distinct()
                .order_by("access_ip")
            )

            return R.success(data=data)
        except Exception as e:
            logger.error(e, exc_info=True)
            return R.success(data=list(), msg=_("failure"))
