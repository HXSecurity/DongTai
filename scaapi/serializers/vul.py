#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 16:13
# software: PyCharm
# project: sca
from rest_framework import serializers

from scaapi.models.artifact import ScaArtifactDb
from scaapi.models.maven_artifact import ScaMavenArtifact


class VulDBSerializer(serializers.ModelSerializer):
    components = serializers.SerializerMethodField()

    class Meta:
        model = ScaArtifactDb
        fields = ['cwe_id', 'cve_id', 'title',
                  'overview', 'teardown', 'latest_version', 'component_name', 'components', 'reference']

    def get_components(self, obj):
        # 根据aid查询组件信息
        artifacts = ScaMavenArtifact.objects.filter(aid=obj.id)
        data = list()
        for artifact in artifacts:
            data.append({
                'groupId': artifact.group_id,
                'artifactId': artifact.artifact_id,
                'version': artifact.version,
                'updateToVersion': artifact.safe_version,
                'type': artifact.type,
                'patch': artifact.patch,
                'signature': artifact.signature
            })
        return data
