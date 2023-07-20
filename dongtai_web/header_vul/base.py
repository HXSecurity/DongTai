import logging

from dongtai_common.endpoint import UserEndPoint, R

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck
from rest_framework.serializers import ValidationError
from rest_framework import viewsets
from dongtai_common.models.header_vulnerablity import (
    IastHeaderVulnerability,
    IastHeaderVulnerabilityDetail,
)
from django.db.models import Q

logger = logging.getLogger("dongtai-webapi")


class HeaderVulArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))
    vul_id = serializers.IntegerField(required=True, help_text=_("Page index"))


class HeaderVulDetailSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source="agent.token")

    class Meta:
        model = IastHeaderVulnerabilityDetail
        fields = ("agent_id", "agent_name", "req_header", "res_header")


class HeaderVulSerializer(serializers.ModelSerializer):
    details = HeaderVulDetailSerializer(
        source="iastheadervulnerabilitydetail_set", many=True
    )

    class Meta:
        model = IastHeaderVulnerability
        fields = ("id", "url", "details")


class HeaderVulViewSet(UserEndPoint, viewsets.ViewSet):
    permission_classes_by_action: dict = {}

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @extend_schema_with_envcheck(
        [HeaderVulArgsSerializer],
        tags=[_("Header Vul")],
        summary=_("Header Vul 列表"),
        description=_("Get the item corresponding to the user"),
    )
    def list(self, request):
        ser = HeaderVulArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page = ser.validated_data["page"]
                page_size = ser.validated_data["page_size"]
                vul_id = ser.validated_data["vul_id"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        department = request.user.get_relative_department()
        q = Q(project__department__in=department) & Q(vul_id=vul_id)
        queryset = IastHeaderVulnerability.objects.filter(q).all()
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(
            data=HeaderVulSerializer(page_data, many=True).data, page=page_summary
        )

    @extend_schema_with_envcheck(
        tags=[_("Header Vul")],
        summary=_("Header Vul 删除"),
        description=_("Get the item corresponding to the user"),
    )
    def delete(self, request, pk):
        HeaderVulArgsSerializer(data=request.GET)
        users = self.get_auth_users(request.user)
        q = Q(project__user__in=users) & Q(pk=pk)
        IastHeaderVulnerability.objects.filter(q).delete()
        return R.success()
