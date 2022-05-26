# 批量删除 组件漏洞+应用漏洞
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.asset_vul import IastVulAssetRelation
from dongtai_common.models.asset_vul_relation import AssetVulRelation
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.models.asset import Asset
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.db import connection
from dongtai_web.aggregation.aggregation_common import turnIntListOfStr
import logging

logger = logging.getLogger('dongtai-dongtai_conf')

class DelVulMany(UserEndPoint):
    name = "api-v2-aggregation-list-del"
    description = _("del vul list of many")

    @extend_schema_with_envcheck(

        tags=[_('VulList')],
        summary=_('Vul List delete'),
        description=_(
            "delete many app vul and dongtai_sca vul"
        ),
    )
    def post(self, request):
        ids = request.data.get("ids","")
        ids = turnIntListOfStr(ids)
        source_type = request.data.get("source_type",1)
        user = request.user
        if source_type == 1:
            queryset = IastVulnerabilityModel.objects.filter(is_del=0)
        else:
            queryset = IastVulAssetRelation.objects.filter(is_del=0)

        # 超级管理员
        if user.is_system_admin():
             pass
        # 租户管理员 or 部门管理员
        elif user.is_talent_admin() or user.is_department_admin:
            users = self.get_auth_users(user)
            user_ids = list(users.values_list('id', flat=True))
            if source_type == 1:
                queryset = queryset.filter(agent__user_id__in=user_ids)
            else:
                queryset = queryset.filter(asset__user_id__in=user_ids)
        else:
            # 普通用户
            if source_type == 1:
                queryset = queryset.filter(agent__user_id=user.id)
            else:
                queryset = queryset.filter(asset__user_id=user.id)

        if source_type==1:
            # 应用漏洞删除
            queryset.filter(id__in=ids).update(is_del=1)
        else:
            # 组件漏洞删除
            queryset.filter(asset_vul_id__in=ids).update(is_del=1)
            # with connection.cursor() as cursor:
            #     sca_ids = list(map(str, ids))
            #     sca_ids_str = ",".join(sca_ids)
            #     sql = " UPDATE iast_asset_aggr as aggr left join iast_asset_vul as vul on aggr.signature_value=vul.package_hash SET aggr.is_del = 1  WHERE vul.id in ({})".format(
            #         sca_ids_str)
            #     cursor.execute(sql)

        return R.success(data={
            'messages': "success",

        }, )