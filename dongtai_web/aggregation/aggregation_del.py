# 批量删除 组件漏洞+应用漏洞
import logging

from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.asset_vul import IastVulAssetRelation
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_web.aggregation.aggregation_common import turnIntListOfStr
from dongtai_web.utils import extend_schema_with_envcheck

logger = logging.getLogger("dongtai-dongtai_conf")


class DelVulMany(UserEndPoint):
    name = "api-v2-aggregation-list-del"
    description = _("del vul list of many")

    @extend_schema_with_envcheck(
        tags=[_("漏洞")],
        summary=_("删除漏洞列表"),
        description=_("delete many app vul and dongtai_sca vul"),
    )
    def post(self, request):
        ids = request.data.get("ids", "")
        ids = turnIntListOfStr(ids)
        source_type = request.data.get("source_type", 1)
        department = request.user.get_relative_department()
        if source_type == 1:
            queryset = IastVulnerabilityModel.objects.filter(is_del=0)
        else:
            queryset = IastVulAssetRelation.objects.filter(is_del=0)

        # 部门删除逻辑
        if source_type == 1:
            queryset = queryset.filter(project__department__in=department)
        else:
            queryset = queryset.filter(asset__department__in=department)

        if source_type == 1:
            # 应用漏洞删除
            del_queryset = queryset.filter(id__in=ids)
        else:
            # 组件漏洞删除
            del_queryset = queryset.filter(asset_vul_id__in=ids)
            # with connection.cursor() as cursor:
            #         sca_ids_str)
        for vul in del_queryset:
            vul.is_del = 1
            vul.save()
        return R.success(
            data={
                "messages": "success",
            },
        )
