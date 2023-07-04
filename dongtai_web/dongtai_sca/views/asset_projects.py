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
from typing import List, Optional, Dict
from drf_spectacular.utils import extend_schema

logger = logging.getLogger(__name__)


class AssetProjects(UserEndPoint):
    name = "api-v1-sca-projects"
    description = ""

    @extend_schema(
        deprecated=True,
        summary="获取组件项目列表",
        tags=["Project"],
    )
    def get(self, request, aggr_id):
        try:
            departments = request.user.get_relative_department()
            asset_queryset = Asset.objects.filter(department__in=departments, is_del=0)
            asset = Asset.objects.filter(id=aggr_id).first()
            #asset_aggr = AssetAggr.objects.filter(
            #    signature_value=asset.signature_value).first()
            if not asset:
                return R.failure(msg=_('Components do not exist or no permission to access'))

            asset_queryset = asset_queryset.filter(
                signature_value=asset.signature_value,
                version=asset.version,
                project_id__gt=0).values('project_id', 'id').all()
            if not asset_queryset:
                return R.failure(msg=_(
                    'Components do not exist or no permission to access'))

            _temp_data = {_a['project_id']: _a['id'] for _a in asset_queryset}
            asset_ids = [_temp_data[p_id] for p_id in _temp_data]

            data = AssetProjectSerializer(
                Asset.objects.filter(pk__in=asset_ids), many=True).data

            return R.success(data=data)
        except Exception as e:
            logger.error(e)
            return R.failure(msg=_('Component projects query failed'))


class AssetVulProjects(UserEndPoint):
    name = "api-v1-sca-vul-projects"
    description = ""

    @extend_schema(
        deprecated=True,
        summary="获取组件漏洞项目列表",
        tags=["Project"],
    )
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
            asset_queryset = asset_queryset.filter(
                iastvulassetrelation__asset_vul_id=vul_id,
                project_id__gt=0).values(
                    'project_id',
                    'project_name',
                    'project_version_id',
            ).distinct().all()

            data = []
            asset_queryset = asset_queryset.order_by('project_id', 'project_version_id')
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('pageSize', 10))
            page_summary, page_data = self.get_paginator(asset_queryset, page, page_size)

            if page_data:
                for _data in page_data:
                    project_version_query = IastProjectVersion.objects.filter(
                        project_id=_data['project_id'],
                        id=_data['project_version_id']).first()
                    if project_version_query:
                        project_version = project_version_query.version_name
                    else:
                        project_version = ''
                    asset_info = asset_queryset.filter(
                        project_id=_data['project_id']).order_by(
                            'level_id').values('level_id').first()
                    level = IastVulLevel.objects.filter(
                        id=asset_info['level_id']).first()
                    #level = IastVulLevel.objects.filter(id=_data['level_id']).first()
                    level_name = level.name_value if level else ""
                    data.append({
                        'project_id':
                        _data['project_id'],
                        'project_name':
                        _data['project_name'],
                        'level':
                        level_name,
                        'project_version':
                        project_version,
                        'dependency_level':
                        0,
                        'project_version_id':
                        _data['project_version_id']
                    })

            return R.success(data=data, page=page_summary)
        except Exception as e:
            logger.error(e)
            return R.failure(msg=_('Component vul projects query failed'))


def get_tree(dep_list: List[str]):
    a = {}
    len_of_list = len(dep_list)
    for ind, i in enumerate(dep_list):
        if a:
            a = {"package_name": i, "dependency_asset": [a], "dependency_level": len_of_list - ind}
        else:
            a = {
                "package_name": i,
                "dependency_level": len_of_list - ind,
            }
    return a

class ProjectsAssets(UserEndPoint):
    name = "api-v1-sca-vul-project-assets"
    description = ""

    @extend_schema(
        deprecated=True,
        summary="获取项目组件列表",
        tags=["Project"],
    )
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
            asset_queryset = asset_queryset.filter(
                iastvulassetrelation__asset_vul_id=vul_id,
                project_id=project_id,
                project_version_id=project_version_id).values(
                    'id', 'dependency_level', 'package_name', 'version',
                    'level', 'parent_dependency_id',
                    'iastvulassetrelation__vul_dependency_path').order_by(
                        'level_id').first()
            if asset_queryset['iastvulassetrelation__vul_dependency_path'] is not None:
                return R.success(data=[get_tree(asset_queryset['iastvulassetrelation__vul_dependency_path'])])
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
            logger.error(e, exc_info=True)
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
