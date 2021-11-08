# coding:utf-8

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project_report import ProjectReport
from dongtai.models.project import IastProject
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck
from rest_framework.serializers import ValidationError


class _ProjectReportSearchQuerysSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    pid = serializers.IntegerField(default=1, help_text=_('Project id'))


class _ProjectReportListDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectReport
        fields = ['id', 'type', 'status', 'create_time']


class ProjectReportList(UserEndPoint):
    name = 'api-v1-report-list'
    description = _('Vulnerability Report List')

    @extend_schema_with_envcheck(
        [_ProjectReportSearchQuerysSerializer],
        tags=[_('Project')],
        summary=_('Projects Report List'),
        description=
        _("According to the conditions, list the report of the specified project or the project of the specified vulnerability."
          ),
    )
    def get(self, request):
        page = request.query_params.get('page', 1)
        pid = request.query_params.get('pid', 0)
        page_size = request.query_params.get('page_size', 20)
        ser = _ProjectReportSearchQuerysSerializer(data=request.data)

        auth_users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(pk=pid, user__in=auth_users).first()
        try:
            if ser.is_valid(True):
                page = ser.validated_data['page']
                page_size = ser.validated_data['page_size']
        except ValidationError as e:
            return R.failure(data=e.detail)
        queryset = ProjectReport.objects.filter(
            user__in=auth_users,
            project=project
        ).order_by('-create_time')

        page_summary, page_data = self.get_paginator(queryset, page, page_size)

        return R.success(data=_ProjectReportListDataSerializer(page_data, many=True).data,
                         page=page_summary)
