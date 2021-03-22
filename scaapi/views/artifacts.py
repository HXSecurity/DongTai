#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 15:31
# software: PyCharm
# project: sca
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from iast.base.user import UserEndPoint
from scaapi.filters.artifact import ArtifactFilter
from scaapi.models.maven_artifact import ScaMavenArtifact
from scaapi.pagination.ScaPageNumberPagination import SCAPageNumberPagination
from scaapi.serializers.artifact import ArtifactSerializer


class ArtifactView(UserEndPoint):
    """
    软件组成分析：查询第三方组件是否存在漏洞

    参数列表：
        - type： 组件管理工具，如：maven、gradle
        - group: 项目的唯一标识符，如：com.fasterxml.jackson.core
        - artifact: 组件的唯一标识符，如；jackson-databind
        - version: 组件的版本，如：2.10.4
        - aql: 组件查询语言，如：maven:com.fasterxml.jackson.core:jackson-databind
        - signature: 组件签名（SHA-1)，如：cac8abd106fab36e6b1e2dd4f58c55ca788761cd

    返回值：
    ```json
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "safe_version": "2.9.10.5",
                "patch": "https://github.com/FasterXML/jackson-databind/commit/f6d9c664f6d481703138319f6a0f1fdbddb3a259",
                "type": "maven",
                "group_id": "com.fasterxml.jackson.core",
                "artifact_id": "jackson-databind",
                "version": "2.9.0",
                "vul": {
                    "cve": "CVE-2020-14195",
                    "cwe": "CWE-502",
                    "title": "Remote Code Execution",
                    "overview": "jackson-databind is vulnerable to remote code execution. It was possible to use the `org.jsecurity` gadget type as a serialization gadget through polymorphic typing and execute arbitrary code on the system.",
                    "teardown": "",
                    "latest_version": "2.11.1",
                    "component_name": "jackson-databind"
                }
            }
        ]
    }
    ```
    """
    queryset = ScaMavenArtifact.objects.all()
    serializer_class = ArtifactSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    pagination_class = SCAPageNumberPagination
    filterset_class = ArtifactFilter
