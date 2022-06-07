# !usr/bin/env python
# coding:utf-8
# @author:zhaoyanwei
# @file: tasks.py
# @time: 2022/5/9  下午3:45

from dongtai_common.models import User
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.asset import Asset
from celery.apps.worker import logger

from dongtai_web.dongtai_sca.utils import sca_scan_asset


def refresh_all_asset_data():
    """
    todo 一次性任务，更新组件数据
    """
    logger.info('开始更新组件数据')

    iast_assets = Asset.objects.filter(dependency_level=0).all()
    if iast_assets:
        for asset in iast_assets:
            try:
                update_fields = []
                asset_agent = IastAgent.objects.filter(id=asset.agent_id).values("bind_project_id",
                                                                                 "project_name",
                                                                                 "user_id",
                                                                                 "project_version_id",
                                                                                 "language").first()
                if asset_agent:
                    if asset_agent['bind_project_id'] != 0:
                        asset.project_id = asset_agent['bind_project_id']
                        asset.project_name = asset_agent['project_name']
                        asset.project_version_id = asset_agent['project_version_id']
                        update_fields.extend(['project_id', 'project_name', 'project_version_id'])
                    if asset_agent['user_id'] != 0:
                        user = User.objects.filter(id=asset_agent['user_id']).first()
                        if user:
                            user_department = user.get_department()
                            user_talent = user.get_talent()
                            asset.department_id = user_department.id if user_department else -1
                            asset.talent_id = user_talent.id if user_talent else -1
                            asset.user_id = asset_agent['user_id']
                            update_fields.append('user_id')
                            update_fields.append('talent_id')
                            update_fields.append('department_id')
                    update_fields.append('language')
                    asset.language = asset_agent['language']

                asset.save(update_fields=update_fields)

                # 更新asset
                sca_scan_asset(asset)

            except Exception as e:
                continue

    logger.info('组件更新数据处理完成')

    return True
