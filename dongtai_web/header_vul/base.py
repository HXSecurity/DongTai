import logging

from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.hook_type import HookType
from dongtai_common.utils import const

from dongtai_web.serializers.hook_type_strategy import HookTypeSerialize
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from rest_framework.serializers import ValidationError
from dongtai_web.serializers.hook_strategy import HOOK_TYPE_CHOICE
from rest_framework import viewsets
from django.db import connection
from django.db import models
from dongtai_common.permissions import TalentAdminPermission
from dongtai_common.models.header_vulnerablity import IastHeaderVulnerability, IastHeaderVulnerabilityDetail
from django.db.models import Q

logger = logging.getLogger('dongtai-webapi')


class HeaderVulArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))

class HeaderVulDetailSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.token')
    class Meta:
        model = IastHeaderVulnerabilityDetail
        fields = ('agent_id', 'agent_name', 'req_header', 'res_header')


class HeaderVulSerializer(serializers.ModelSerializer):
    details = HeaderVulDetailSerializer(source='iastheadervulnerabilitydetail_set',many=True)

    class Meta:
        model = IastHeaderVulnerability
        fields = ('url', 'details')



class HeaderVulViewSet(UserEndPoint, viewsets.ViewSet):

    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            return [
                permission() for permission in
                self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def list(self, request):
        ser = HeaderVulArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page = ser.validated_data['page']
                page_size = ser.validated_data['page_size']
                vul_id = ser.validated_data['vul_id']
        except ValidationError as e:
            return R.failure(data=e.detail)
        users = self.get_auth_users(request.user)
        q = Q(project__user__in=users) & Q(vul_id=vul_id)
        queryset = IastHeaderVulnerability.objects.filter(q).all()
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(data=HeaderVulSerializer(page_data, many=True).data,
                         page=page_summary)
