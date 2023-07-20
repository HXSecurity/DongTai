#!/usr/bin/env python
# datetime:2020/6/3 11:36
from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.deploy import IastDeployDesc
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck


class AgentDeployDesc(UserEndPoint):
    name = "api-v1-iast-deploy-desc"
    description = _("Agent deployment document")

    @extend_schema_with_envcheck(
        [{"name": "os", "type": str}, {"name": "server", "type": str}]
    )
    def get(self, request):
        queryset = IastDeployDesc.objects.all()

        os = request.query_params.get("os", "linux")
        if os:
            queryset = queryset.filter(os=os)

        middle = request.query_params.get("server", "tomcat")
        if middle:
            queryset = queryset.filter(middleware=middle)

        queryset = queryset.last()
        if queryset:
            return R.success(msg=queryset.desc)
        else:
            return R.failure(msg=_("No data"))
