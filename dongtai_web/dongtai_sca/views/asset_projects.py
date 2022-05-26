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
from dongtai_web.dongtai_sca import AssetProjectSerializer

logger = logging.getLogger(__name__)


class AssetProjects(UserEndPoint):
    name = "api-v1-sca-projects"
    description = ""

    def get(self, request, aggr_id):
        try:
            auth_users = self.get_auth_users(request.user)
            asset_queryset = self.get_auth_assets(auth_users)
            asset_aggr = AssetAggr.objects.filter(id=aggr_id).first()
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


class AssetVulProjects(UserEndPoint):
    name = "api-v1-sca-vul-projects"
    description = ""

    def get(self, request, vul_id):
        try:
            auth_users = self.get_auth_users(request.user)
            asset_queryset = self.get_auth_assets(auth_users)
            asset_vul = IastAssetVul.objects.filter(id=vul_id).first()
            if not asset_vul:
                return R.failure(msg=_('Components of the vul do not exist or no permission to access'))

            package_kw = request.query_params.get('keyword', None)

            if package_kw and package_kw.strip() != '':
                asset_queryset = asset_queryset.filter(project_name__icontains=package_kw)

            # todo 是否限制只展示4层以内的项目
            asset_queryset = asset_queryset.filter(dependency_level__gt=0,
                                                   signature_value=asset_vul.package_hash,
                                                   package_name=asset_vul.package_name,
                                                   version=asset_vul.package_version, project_id__gt=0).values(
                'project_id',
                'project_name',
                'project_version_id',
                'dependency_level',
                'level_id').all()

            data = []
            asset_queryset = asset_queryset.order_by('project_id', 'project_version_id')
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('pageSize', 10)
            page_summary, page_data = self.get_paginator(asset_queryset, page, page_size)

            if page_data:
                for _data in page_data:
                    project_version_query = IastProjectVersion.objects.filter(project_id=_data['project_id'],
                                                                              id=_data['project_version_id']).first()
                    if project_version_query:
                        project_version = project_version_query.version_name
                    else:
                        project_version = ''
                    level = IastVulLevel.objects.filter(id=_data['level_id']).first()
                    level_name = level.name_value if level else ""
                    data.append(
                        {'project_id': _data['project_id'], 'project_name': _data['project_name'], 'level': level_name,
                         'project_version': project_version, 'dependency_level': _data['dependency_level'],
                         'project_version_id': _data['project_version_id']})

            return R.success(data=data, page=page_summary)
        except Exception as e:
            logger.error(e)
            return R.failure(msg=_('Component vul projects query failed'))


class ProjectsAssets(UserEndPoint):
    name = "api-v1-sca-vul-project-assets"
    description = ""

    def get(self, request):

        try:
            auth_users = self.get_auth_users(request.user)
            asset_queryset = self.get_auth_assets(auth_users)

            vul_id = request.query_params.get('vul_id', 0)
            project_id = request.query_params.get('project_id', 0)
            project_version_id = request.query_params.get('project_version_id', 0)

            if not project_id:
                return R.failure(msg=_('Param error'))

            asset_vul = IastAssetVul.objects.filter(id=vul_id).first()
            if not asset_vul:
                return R.failure(msg=_('Vul not exist'))

            # 当前漏洞所在组件
            asset_queryset = asset_queryset.filter(package_name=asset_vul.package_name,
                                                   version=asset_vul.package_version,
                                                   signature_value=asset_vul.package_hash, project_id=project_id,
                                                   project_version_id=project_version_id).values('id',
                                                                                                 'dependency_level',
                                                                                                 'package_name',
                                                                                                 'version',
                                                                                                 'level',
                                                                                                 'parent_dependency_id').first()

            dependency_level = asset_queryset['dependency_level']
            parent_dependency_id = asset_queryset['parent_dependency_id']
            LEVEL_MAPS = dict()
            if asset_queryset['level'] not in LEVEL_MAPS:
                asset_level = IastVulLevel.objects.filter(id=asset_queryset['level']).values('id',
                                                                                             'name_value').first()
            else:
                asset_level = LEVEL_MAPS[asset_queryset['level']]
            asset_queryset['level_id'] = asset_level['id']
            asset_queryset['level'] = asset_level['name_value']
            asset_queryset['dependency_asset'] = []

            resp_data = asset_queryset
            asset_queryset_dependency = dict()
            if dependency_level > 1 and parent_dependency_id > 0:
                dependency_asset = _get_parent_dependency(asset_queryset_dependency, parent_dependency_id)
                if dependency_asset:
                    for dependency_key in dependency_asset:
                        if dependency_asset[dependency_key]['level'] not in LEVEL_MAPS:
                            asset_level = IastVulLevel.objects.filter(
                                id=dependency_asset[dependency_key]['level']).values('id', 'name_value').first()
                        else:
                            asset_level = LEVEL_MAPS[asset_queryset['level']]

                        dependency_asset[dependency_key]['level_id'] = asset_level['id']
                        dependency_asset[dependency_key]['level'] = asset_level['name_value']

                        if dependency_key + 1 not in dependency_asset:
                            dependency_asset[dependency_key]['dependency_asset'] = [asset_queryset]
                        else:
                            dependency_key_n = dependency_key + 1
                            dependency_asset[dependency_key]['dependency_asset'] = [dependency_asset[dependency_key_n]]
                    resp_data = dependency_asset[1]

            return R.success(data=[resp_data])
        except Exception as e:
            logger.error(e)
            return R.failure(msg=_('Component vul projects query failed'))


def _get_parent_dependency(asset_queryset_dependency, parent_dependency_id):
    parent_asset = Asset.objects.filter(id=parent_dependency_id).values('id', 'dependency_level', 'package_name',
                                                                        'version', 'level',
                                                                        'parent_dependency_id').first()
    if parent_asset:
        dependency_level = parent_asset['dependency_level']
        parent_dependency_id = parent_asset['parent_dependency_id']
        asset_queryset_dependency[dependency_level] = parent_asset
        if dependency_level > 1 and parent_dependency_id > 0:
            _get_parent_dependency(asset_queryset_dependency, parent_dependency_id)

    return asset_queryset_dependency
