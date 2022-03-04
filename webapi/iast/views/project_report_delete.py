# coding:utf-8

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project_report import ProjectReport
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
import os
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework.serializers import ValidationError


class _ProjectReportSearchQuerysSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=0,
                                  help_text=_('The id of the project report'))


_GetResponseSerializer = get_response_serializer(_ProjectReportSearchQuerysSerializer())


class ProjectReportDelete(UserEndPoint):
    name = 'api-v1-report-delete'
    description = _('Delete Vulnerability Report')

    @extend_schema_with_envcheck(
        request=_ProjectReportSearchQuerysSerializer,
        tags=[_('Project')],
        summary=_('Projects Report Export'),
        description=
        _("According to the conditions, delete the report of the specified project or the project of the specified vulnerability."
          ),
        response_schema=_GetResponseSerializer,
    )
    def post(self, request):
        id = 0
        ser = _ProjectReportSearchQuerysSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                id = ser.validated_data['id']
        except ValidationError as e:
            return R.failure(data=e.detail)

        record = ProjectReport.objects.filter(
            id=id,
            user=request.user,
        ).first()

        if record:
            if record.path:
                os.remove(record.path)
            record.delete()
        return R.success(msg=_('Deleted Successfully'))
