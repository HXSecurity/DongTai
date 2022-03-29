# coding:utf-8

import time

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project_report import ProjectReport
from dongtai.models.project import IastProject
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck
from rest_framework.serializers import ValidationError
from django.utils.translation import get_language


class _ProjectReportExportQuerySerializer(serializers.Serializer):
    vid = serializers.IntegerField(
        help_text=_("The vulnerability id of the project"), required=False)
    pname = serializers.CharField(
        help_text=_("The name of the project"), required=False)
    pid = serializers.IntegerField(help_text=_("The id of the project"), required=False)
    type = serializers.CharField(
        help_text=_("The type of the vulnerability report"), required=False)


class ProjectReportSyncAdd(UserEndPoint):
    name = 'api-v1-report-sync-add'
    description = _('Vulnerability Report Async Export')

    @extend_schema_with_envcheck(
        request=_ProjectReportExportQuerySerializer,
        tags=[_('Project')],
        summary=_('Vulnerability Report Async Export'),
        description=
        _("According to the conditions, export the report of the specified project or the project of the specified vulnerability async."
          ),
    )
    def post(self, request):
        timestamp = time.time()
        pid = vid = 0
        pname = type = ""
        ser = _ProjectReportExportQuerySerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pid = int(request.data.get("pid", 0))
                pname = request.data.get('pname')
                vid = int(request.data.get("vid", 0))
                type = request.data.get("type", "docx")
        except ValidationError as e:
            return R.failure(data=e.detail)

        if (pid == 0 and pname == ''):
            return R.failure(status=202, msg=_('Parameter error'))
        auth_users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(pk=pid, user__in=auth_users).first()
        if not project:
            return R.failure(status=202, msg=_('Project not exist'))
        if type not in ['docx', 'pdf', 'xlsx']:
            return R.failure(status=202, msg=_('Report type error'))
        ProjectReport.objects.create(
            user=request.user, project=project, vul_id=vid,
            status=0, type=type, create_time=timestamp, language=get_language()
        )

        return R.success(msg=_('Created success'))
