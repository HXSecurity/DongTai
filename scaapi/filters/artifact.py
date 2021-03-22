#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 15:26
# software: PyCharm
# project: sca
from django_filters import rest_framework as filters

from scaapi.models.maven_artifact import ScaMavenArtifact


# https://docs.djangoproject.com/en/3.1/ref/models/querysets/#field-lookups
class ArtifactFilter(filters.FilterSet):
    type = filters.CharFilter(field_name="type", label="组件管理工具")
    group = filters.CharFilter(field_name="group_id", label="组件所属组")
    artifact = filters.CharFilter(field_name="artifact_id", label="组件标识")
    version = filters.CharFilter(field_name="version", label="组件版本")
    aql = filters.CharFilter(field_name="cph_version", label='组件查询语句', lookup_expr='icontains')
    hash = filters.CharFilter(field_name="signature", label='组件哈希值（SHA-1）')

    class Meta:
        model = ScaMavenArtifact
        fields = ['type', 'group', 'artifact', 'version', 'aql', 'hash']
