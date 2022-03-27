# coding:utf-8

import time

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project_report import ProjectReport
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck
from django.http import HttpResponse
from io import BytesIO
from rest_framework.serializers import ValidationError


class _ProjectReportSearchQuerysSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=0,
                                  help_text=_('The id of the project report'))


class ProjectReportDownload(UserEndPoint):
    name = 'api-v1-report-download'
    description = _('Vulnerability Report Download')

    @extend_schema_with_envcheck(
        [_ProjectReportSearchQuerysSerializer],
        tags=[_('Project')],
        summary=_('Projects Report Download'),
        description=
        _("According to the conditions, export the report of the specified project or the project of the specified vulnerability."
          ),
    )
    def get(self, request):
        id = 0
        ser = _ProjectReportSearchQuerysSerializer(data=request.query_params)
        try:
            if ser.is_valid(True):
                id = ser.validated_data['id']
        except ValidationError as e:
            return R.failure(data=e.detail)

        record = ProjectReport.objects.filter(id=id,
                                              user=request.user,
                                              status=1).only(
                                                  'file',
                                                  'project__name').first()

        if not record:
            return R.failure(msg=_('No data'))

        if record.status != 1:
            return R.failure(msg=_('Record is not ready'))

        report_filename = '{}.{}'.format(record.project.name, record.type)

        response = HttpResponse(record.file)
        response['Content-Disposition'] = f'attachment; filename="{report_filename}"'
        return response
