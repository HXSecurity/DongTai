#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 18:13
# software: PyCharm
# project: sca
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from iast.base.user import UserEndPoint
from scaapi.filters.vul import VulFilter
from scaapi.models.artifact import ScaArtifactDb
from scaapi.pagination.ScaPageNumberPagination import SCAPageNumberPagination
from scaapi.serializers.vul import VulDBSerializer


class VulsView(UserEndPoint):
    """
    软件组成分析：根据CVE编号查询

    参数列表：
        - cve: cve编号，如：CVE-2020-7961
        - type： 漏洞类型，如：rce
        - group: 项目的唯一标识符，如：com.fasterxml.jackson.core
        - artifact: 组件的唯一标识符，如；jackson-databind
        - artifact_name: 组件名称，如：jackson

    返回值：
    ```json
    {
      "cwe_id": "CWE-20",
      "cve_id": "CVE-2020-11975",
      "title": "Arbitrary Code Execution",
      "overview": "unomi-plugins-base is vulnerable to arbitrary code execution. The vulnerability exists due to the lack of checks on the permitted classes to be executed when evaluating a property condition.",
      "teardown": "",
      "latest_version": "1.5.1",
      "component_name": "Apache Unomi :: Plugins :: Base Actions and Conditions",
      "components": [
        {
          "groupId": "org.apache.unomi",
          "artifactId": "unomi-plugins-base",
          "version": "1.0.0-incubating",
          "updateToVersion": "1.5.1",
          "type": "maven",
          "patch": "https://github.com/apache/unomi/commit/789ae8e820c507866b9c91590feebffa4e996f5e"
        },
      ]
    }
    ```
    """
    queryset = ScaArtifactDb.objects.all()
    serializer_class = VulDBSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    pagination_class = SCAPageNumberPagination
    filterset_class = VulFilter
