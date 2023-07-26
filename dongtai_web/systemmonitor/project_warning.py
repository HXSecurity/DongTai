import json
import logging

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.profile import IastProfile
from dongtai_common.utils.request_type import Request
from dongtai_engine.plugins.project_status import (
    PROJECT_WARNING_TIME_KEY,
    get_project_warning_time,
)
from dongtai_web.utils import extend_schema_with_envcheck

logger = logging.getLogger("django")


class ProjectWarningSettingsSer(serializers.Serializer):
    error_time = serializers.IntegerField()
    offline_time = serializers.IntegerField()


class ProjectWarningEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(
        summary=_("Get Profile"),
        description=_("Get Profile with key"),
        tags=[_("Profile")],
    )
    def get(self, request: Request) -> JsonResponse:
        return R.success(data=get_project_warning_time())

    @extend_schema_with_envcheck(
        summary=_("Profile modify"),
        request=ProjectWarningSettingsSer,
        description=_("Modifiy Profile with key"),
        tags=[_("Profile")],
    )
    def post(self, request: Request) -> JsonResponse:
        ser = ProjectWarningSettingsSer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except serializers.ValidationError as e:
            return R.failure(data=e.detail)

        try:
            IastProfile.objects.update_or_create(
                {"key": PROJECT_WARNING_TIME_KEY, "value": json.dumps(ser.data)},
                key=PROJECT_WARNING_TIME_KEY,
            )
        except Exception as e:
            logger.exception("exception: ", exc_info=e)
            return R.failure(msg=_("Update {} failed").format(PROJECT_WARNING_TIME_KEY))

        return R.success(data=ser.data)
