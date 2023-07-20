# 批量删除 组件漏洞+应用漏洞
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.asset_vul import IastVulAssetRelation

from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck
import logging

logger = logging.getLogger("dongtai-dongtai_conf")


class DelVulProjectLevel(UserEndPoint):
    name = "api-v2-project-del"
    description = _("del vul list of many")

    @extend_schema_with_envcheck(
        tags=[_("漏洞")],
        summary=_("删除 Vul List"),
        description=_("delete many app vul and dongtai_sca vul"),
    )
    def post(self, request):
        project_id = request.data.get("project_id", None)
        if project_id is None:
            return R.failure()
        project_version_id = request.data.get("project_version_id", None)
        source_type = request.data.get("source_type", 1)
        department = request.user.get_relative_department()
        if source_type == 1:
            queryset = IastVulnerabilityModel.objects.filter(is_del=0)
        else:
            queryset = IastVulAssetRelation.objects.filter(is_del=0)
        # 部门删除逻辑
        if source_type == 1:
            queryset = queryset.filter(project_id__in=[project_id])
        else:
            queryset = queryset.filter(asset__project_id__in=[project_id])
        if project_version_id:
            if source_type == 1:
                queryset = queryset.filter(project_version_id__in=[project_version_id])
            else:
                queryset = queryset.filter(
                    asset__project_version_id__in=[project_version_id]
                )

        # 部门删除逻辑
        if source_type == 1:
            queryset = queryset.filter(project__department__in=department)
        else:
            queryset = queryset.filter(asset__department__in=department)

        for vul in queryset:
            vul.is_del = 1
            vul.save()
        return R.success(
            data={
                "messages": "success",
            },
        )
