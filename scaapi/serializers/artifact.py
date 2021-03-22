#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 15:33
# software: PyCharm
# project: sca
import json

from rest_framework import serializers

from scaapi.models.artifact import ScaArtifactDb
from scaapi.models.maven_artifact import ScaMavenArtifact


class ArtifactSerializer(serializers.ModelSerializer):
    vul = serializers.SerializerMethodField()

    class Meta:
        model = ScaMavenArtifact
        fields = ['safe_version', 'patch', 'type',
                  'group_id', 'artifact_id', 'version', 'vul', 'signature', 'package_name']
        # fields = '__all__'

    def get_vul(self, artifact_obj):
        _vuls = ScaArtifactDb.objects.filter(pk=artifact_obj.aid)
        if len(_vuls) > 0:
            _vul = _vuls[0]
            _vul_data = {
                "cve": _vul.cve_id,
                "cwe": _vul.cwe_id,
                "title": _vul.title,
                "overview": _vul.overview,
                "teardown": _vul.teardown,
                "latest_version": _vul.latest_version,
                "component_name": _vul.component_name,
                "reference": _vul.reference
            }
            return _vul_data
        else:
            return {
                "cve": '',
                "cwe": '',
                "title": '',
                "overview": '',
                "teardown": '',
                "latest_version": '',
                "component_name": '',
                "reference": json.dumps([])
            }
