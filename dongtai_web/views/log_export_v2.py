from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from import_export import resources
from rest_framework import serializers
from rest_framework.request import Request

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.log import IastLog
from dongtai_common.models.user import User


class _LogsDeleteSerializer(serializers.Serializer):
    ids = serializers.Field(default=None, help_text=_("Log ids to delete"))


class LogResurce(resources.ModelResource):
    def get_export_headers(self):
        return [
            "时间",
            "URL",
            "Raw URL",
            "模块名称",
            "功能名称",
            "操作类型",
            "用户",
            "访问IP地址",
        ]

    class Meta:
        model = IastLog
        fields = (
            "action_time",
            "url",
            "raw_url",
            "module_name",
            "function_name",
            "operate_type",
            "user",
            "access_ip",
        )


class LogExportV2(UserEndPoint):
    resource_class = LogResurce

    @staticmethod
    def attachment_response(
        export_data,
        filename: str = "download.xls",
        content_type: str = "application/vnd.ms-excel",
    ) -> HttpResponse:
        """
        - https://segmentfault.com/q/1010000009719860
        - https://blog.csdn.net/qq_34309753/article/details/99628474
        """
        response = HttpResponse(export_data, content_type=content_type)
        response["content_type"] = content_type
        response["Content-Disposition"] = "attachment; filename*=utf-8''{}".format(
            escape_uri_path(filename)
        )
        return response

    @extend_schema(
        parameters=[_LogsDeleteSerializer],
        description="Export Logs.",
        summary="Export Logs",
        tags=["Logs"],
    )
    def get(self, request: Request) -> HttpResponse:
        ids: str | None = request.query_params.get("ids")
        if ids:
            id_list = [int(id.strip()) for id in ids.split(",")]
            user: User = request.user  # type: ignore
            if user.is_system_admin():
                queryset = IastLog.objects.filter(id__in=id_list).filter()
            elif user.is_talent_admin():
                auth_users = UserEndPoint.get_auth_users(user)
                queryset = IastLog.objects.filter(
                    id__in=id_list, user__in=auth_users
                ).filter()
            else:
                return R.failure(msg=_("no permission"))
            resources = self.resource_class()
            export_data = resources.export(queryset, False)
            return self.attachment_response(
                getattr(export_data, "xls"), filename="用户操作日志.xls"
            )
        else:
            return R.failure(
                status=202,
                msg=_("Export failed, error message: Log id should not be empty"),
            )
