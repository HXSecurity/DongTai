# !usr/bin/env python
# coding:utf-8
# @author:zhaoyanwei
# @file: asset_projects.py
# @time: 2022/5/7  上午7:18
import logging

from django.db.models import Count
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models import User
from dongtai_common.models.asset import Asset
from dongtai_common.models.asset_aggr import AssetAggr
from dongtai_common.models.asset_vul import IastAssetVul
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_web.serializers.sca import ScaSerializer
from dongtai_web.dongtai_sca.serializers.asset_project import AssetProjectSerializer

logger = logging.getLogger(__name__)


class AssetProjects(UserEndPoint):
    name = "api-v1-sca-projects"
    description = ""

    def get(self, request, aggr_id):
        try:
            auth_users = self.get_auth_users(request.user)
            asset_queryset = self.get_auth_assets(auth_users)
            asset = Asset.objects.filter(id=aggr_id).first()
            asset_aggr = AssetAggr.objects.filter(
                signature_value=asset.signature_value).first()
            if not asset_aggr:
                return R.failure(msg=_('Components do not exist or no permission to access'))

            asset_queryset = asset_queryset.filter(signature_value=asset_aggr.signature_value, dependency_level__gt=0,
                                                   version=asset_aggr.version, project_id__gt=0).values('project_id',
                                                                                                        'id').all()
            if not asset_queryset:
                return R.failure(msg=_('Components do not exist or no permission to access'))

            _temp_data = {_a['project_id']: _a['id'] for _a in asset_queryset}
            asset_ids = [_temp_data[p_id] for p_id in _temp_data]

            data = AssetProjectSerializer(Asset.objects.filter(pk__in=asset_ids), many=True).data

            return R.success(data=data)
        except Exception as e:
            logger.error(e)
            return R.failure(msg=_('Component projects query failed'))
