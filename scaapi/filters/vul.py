#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 15:26
# software: PyCharm
# project: sca
from django_filters import rest_framework as filters

from scaapi.models.artifact import ScaArtifactDb


# https://docs.djangoproject.com/en/3.1/ref/models/querysets/#field-lookups
class VulFilter(filters.FilterSet):
    cve = filters.CharFilter(field_name="cve_id", label="CVE编号", lookup_expr='icontains')
    type = filters.CharFilter(field_name="title", label="漏洞类型", lookup_expr='icontains')
    group = filters.CharFilter(field_name="group_id", label="组件所属组")
    artifact = filters.CharFilter(field_name="artifact_id", label="组件标识")
    artifact_name = filters.CharFilter(field_name="component_name", label='组件名称', lookup_expr='icontains')

    class Meta:
        model = ScaArtifactDb
        fields = ['cve', 'type', 'group', 'artifact', 'artifact_name']
