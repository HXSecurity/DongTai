#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/26 11:15
# software: PyCharm
# project: sca
from rest_framework.response import Response

from iast.base.user import UserEndPoint
from scaapi.models.maven_artifact import ScaMavenArtifact


class VulCountView(UserEndPoint):
    def get(self, request, *args, **kwargs):
        res = {"status": 201, "count": 0}
        sign = request.query_params.get('signature', '')
        vul_count = ScaMavenArtifact.objects.filter(signature=sign).count()
        res['count'] = vul_count
        return Response(res)
