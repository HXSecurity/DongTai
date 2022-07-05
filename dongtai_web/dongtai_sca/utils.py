# !usr/bin/env python
# coding:utf-8
# @author:zhaoyanwei
# @file: utils.py
# @time: 2022/5/5  下午7:26
import json
import logging
import random
import time

import requests
from django.conf import settings
from django.db.models import Count, Q
from django.forms import model_to_dict

from dongtai_common.models import User
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.asset import Asset
from dongtai_common.models.asset_aggr import AssetAggr
from dongtai_common.models.asset_vul import IastAssetVul, IastVulAssetRelation, IastAssetVulType, \
    IastAssetVulTypeRelation
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_web.vul_log.vul_log import log_asset_vul_found
from dongtai_web.dongtai_sca.models import Package, VulPackage, VulCveRelation, PackageLicenseLevel, PackageDependency
from dongtai_common.models.asset_vul import IastAssetVulnerabilityDocument
from dongtai_conf.settings import ELASTICSEARCH_STATE

logger = logging.getLogger(__name__)


def sca_scan_asset(asset):
    """
    根据SCA数据库，更新SCA记录信息
    :return:
    """
    agent = asset.agent
    version = asset.version
    asset_package = Package.objects.filter(hash=asset.signature_value, version=version).first()
    update_fields = list()
    try:
        logger.info('[sca_scan_asset]开始检测组件:{}/{}'.format(asset.id, asset.package_name))
        if asset_package:
            package_name = asset_package.aql
            version = asset_package.version

            if version:
                version_code = ""
                version_list = asset_package.version.split('.')[0:4]
                while len(version_list) != 5:
                    version_list.append("0")
                for _version in version_list:
                    version_code += _version.zfill(5)
            else:
                version_code = "0000000000000000000000000"

            vul_list = VulPackage.objects.filter(ecosystem=asset_package.ecosystem, name=asset_package.name,
                                                 introduced=asset_package.version).all()

            if asset_package.license:
                asset.license = asset_package.license
                update_fields.append('license')
            # 最小修复版本-安全版本
            package_ranges = VulPackage.objects.filter(ecosystem=asset_package.ecosystem,
                                                       name=asset_package.name,
                                                       safe_vcode__gte=version_code).order_by("safe_vcode").first()
            if package_ranges and asset.safe_version != package_ranges.safe_version:
                asset.safe_version = package_ranges.fixed
                update_fields.append('safe_version')

            # 最新版本
            last_package = Package.objects.filter(Q(ecosystem=asset_package.ecosystem) &
                                                  Q(name=asset_package.name) & ~Q(version="")).order_by(
                "-version_publish_time").first()
            if last_package:
                asset.last_version = last_package.version
                update_fields.append('last_version')

            levels_dict = dict()
            vul_count = 0
            levels = []
            vul_records = []
            for vul in vul_list:
                if vul.cve in vul_records:
                    continue
                vul_records.append(vul.cve)

                _level = vul.severity
                vul_cve_code = vul.cve
                if vul_cve_code:
                    cve_relation = VulCveRelation.objects.filter(
                        Q(cve=vul_cve_code) | Q(cnvd=vul_cve_code) | Q(cnnvd=vul_cve_code)).first()
                    if cve_relation:
                        if _level == 'note':
                            _level = 'info'
                        if _level and _level not in levels:
                            levels.append(_level)
                        if _level not in levels_dict:
                            levels_dict[_level] = 1
                        else:
                            levels_dict[_level] += 1
                        vul_count += 1
                        # 写入IastAssetVul
                        _add_vul_data(asset, asset_package, cve_relation)

            if len(levels) > 0:
                if 'critical' in levels:
                    level = 'high'
                elif 'high' in levels:
                    level = 'high'
                elif 'medium' in levels:
                    level = 'medium'
                elif 'low' in levels:
                    level = 'low'
                else:
                    level = 'info'
            else:
                level = 'info'

            new_level = IastVulLevel.objects.get(name=level)
            # 更新漏洞等级和各级漏洞数
            if asset.level != new_level:
                asset.level = new_level
                update_fields.append('level')

            if 'critical' in levels_dict:
                asset.vul_critical_count = levels_dict['critical']
                update_fields.append('vul_critical_count')
            else:
                asset.vul_critical_count = 0
                update_fields.append('vul_critical_count')
            if 'high' in levels_dict:
                asset.vul_high_count = levels_dict['high']
                update_fields.append('vul_high_count')
            else:
                asset.vul_high_count = 0
                update_fields.append('vul_high_count')
            if 'medium' in levels_dict:
                asset.vul_medium_count = levels_dict['medium']
                update_fields.append('vul_medium_count')
            else:
                asset.vul_medium_count = 0
                update_fields.append('vul_medium_count')

            if 'low' in levels_dict:
                asset.vul_low_count = levels_dict['low']
                update_fields.append('vul_low_count')
            else:
                asset.vul_low_count = 0
                update_fields.append('vul_low_count')

            if 'info' in levels_dict:
                asset.vul_info_count = levels_dict['info']
                update_fields.append('vul_info_count')
            else:
                asset.vul_info_count = 0
                update_fields.append('vul_info_count')

            if asset.vul_count != vul_count:
                asset.vul_count = vul_count
                update_fields.append('vul_count')

            if asset.package_name != package_name:
                asset.package_name = package_name
                update_fields.append('package_name')

            if asset.version != version:
                asset.version = version
                update_fields.append('version')

            asset.dependency_level = 1
            update_fields.append('dependency_level')

            if len(update_fields) > 0:
                logger.info(f'update asset {asset.id}  dependency fields: {update_fields}')
                asset.save(update_fields=update_fields)
        else:
            logger.warning('[sca_scan_asset]检测组件在组件库不存在:{}/{}'.format(asset.id, asset.package_name))
        update_asset_aggr(asset)
    except Exception as e:
        # import traceback
        # traceback.print_exc()
        logger.info("get package_vul failed:{}".format(e))


# 处理IastAssetVul
def _add_vul_data(asset, asset_package, cve_relation):
    try:
        level_maps = dict()
        _level = cve_relation.severity
        vul_title = ''
        vul_detail = ''
        vul_have_poc = 0
        # vul_have_article = 1 if vul_info['references'] else 0
        vul_have_article = 0

        vul_serial = ''
        vul_reference = dict()
        vul_type_ids = []
        # cve_relation_id = 0
        default_cwe_info = {'cwe_id': '', 'name_chinese': '未知'}

        if cve_relation:
            # cve_relation_id = cve_relation.id
            vul_title = cve_relation.vul_title
            if cve_relation.description:
                vul_detail = cve_relation.description[0]['content']
            vul_have_poc = 1 if cve_relation.poc else 0
            vul_reference = {"cve": cve_relation.cve, "cwe": cve_relation.cwe, "cnnvd": cve_relation.cnnvd,
                             "cnvd": cve_relation.cnvd}
            vul_serial = ' | '.join([vul_reference[_i] for _i in vul_reference])
            vul_serial = vul_title + ' | ' + vul_serial
            vul_cwe_id = cve_relation.cwe.split(',')
            vul_type_cwe = IastAssetVulType.objects.filter(cwe_id__in=vul_cwe_id).all()

            if not vul_type_cwe:
                if cve_relation.cwe_info:
                    for cwe in cve_relation.cwe_info:
                        vul_type_cwe1 = IastAssetVulType.objects.filter(cwe_id=cwe['cwe_id']).first()
                        if not vul_type_cwe1:
                            vul_type_cwe_new = IastAssetVulType.objects.create(cwe_id=cwe['cwe_id'],
                                                                               name=cwe['name_chinese'])
                            vul_type_id = vul_type_cwe_new.id
                        else:
                            vul_type_id = vul_type_cwe1.id
                        vul_type_ids.append(vul_type_id)
            else:
                for cwe in vul_type_cwe:
                    vul_type_ids.append(cwe.id)

        if not vul_type_ids:
            vul_type_cwe = IastAssetVulType.objects.filter(cwe_id=default_cwe_info['cwe_id']).first()
            if not vul_type_cwe:
                vul_type_cwe_new = IastAssetVulType.objects.create(cwe_id=default_cwe_info['cwe_id'],
                                                                   name=default_cwe_info['name_chinese'])
                vul_type_ids.append(vul_type_cwe_new.id)
            else:
                vul_type_ids.append(vul_type_cwe.id)

        vul_license = asset_package.license
        vul_aql = asset_package.aql
        vul_package_hash = asset_package.hash
        vul_package_v = asset_package.version
        vul_package_safe_version = asset.safe_version
        vul_package_latest_version = asset.last_version
        vul_package_language = asset.language

        license_level_info = PackageLicenseLevel.objects.filter(identifier=vul_license).first()
        vul_license_level = license_level_info.level_id if license_level_info else 0

        if _level in level_maps:
            vul_level = level_maps[_level]
        else:
            level_obj = IastVulLevel.objects.filter(name=_level).first()
            if level_obj:
                level_maps[_level] = level_obj.id
                vul_level = level_obj.id
            else:
                vul_level = 1  # critical IastVulLevel查不到归到high
        asset_vul = IastAssetVul.objects.filter(cve_id=cve_relation.id, aql=vul_aql,
                                                package_hash=vul_package_hash,
                                                package_version=vul_package_v).first()
        timestamp = int(time.time())
        if not asset_vul:
            asset_vul = IastAssetVul.objects.create(
                package_name=asset_package.name,
                level_id=vul_level,
                license=vul_license,
                license_level=vul_license_level,
                vul_name=vul_title,
                vul_detail=vul_detail,
                aql=vul_aql,
                package_hash=vul_package_hash,
                package_version=vul_package_v,
                package_safe_version=vul_package_safe_version,
                package_latest_version=vul_package_latest_version,
                package_language=vul_package_language,
                have_article=vul_have_article,
                have_poc=vul_have_poc,
                cve_id=cve_relation.id,
                cve_code=cve_relation.cve,
                vul_cve_nums=vul_reference,
                vul_serial=vul_serial,
                vul_publish_time=cve_relation.publish_time,
                vul_update_time=cve_relation.update_time,
                update_time=timestamp,
                update_time_desc=-timestamp,
                create_time=timestamp
            )
            _add_asset_vul_relation(asset_vul)
            if vul_type_ids:
                type_relation_obj = []
                for vul_type_id in vul_type_ids:
                    type_relation = IastAssetVulTypeRelation(asset_vul_id=asset_vul.id,
                                                             asset_vul_type_id=vul_type_id)
                    type_relation_obj.append(type_relation)

                IastAssetVulTypeRelation.objects.bulk_create(type_relation_obj)

            # new vul add log
            log_project_name = asset.project_name if asset.project_name else ''
            log_project_id = asset.project_id if asset.project_id else 0
            log_user_id = asset.user_id if asset.user_id else 0
            log_asset_vul_found(log_user_id, log_project_name, log_project_id, asset_vul.id, asset_vul.vul_name)
        else:
            asset_vul.update_time = timestamp
            asset_vul.update_time_desc = -timestamp
            asset_vul.save()
            # vul log
            log_project_name = asset.project_name if asset.project_name else ''
            log_project_id = asset.project_id if asset.project_id else 0
            log_user_id = asset.user_id if asset.user_id else 0
            log_asset_vul_found(log_user_id, log_project_name, log_project_id, asset_vul.id, asset_vul.vul_name)
            _add_asset_vul_relation(asset_vul)

    except Exception as e:
        # import traceback
        # traceback.print_exc()
        logger.info("_add_vul_data failed:{}".format(e))


def _add_asset_vul_relation(asset_vul):
    vul_assets = Asset.objects.filter(version=asset_vul.package_version,
                                      signature_value=asset_vul.package_hash).values('id').all()
    asset_vul_relations = []
    timestamp = int(time.time())
    if vul_assets:
        for asset_vl in vul_assets:
            relation_exist = IastVulAssetRelation.objects.filter(asset_vul_id=asset_vul.id,
                                                                 asset_id=asset_vl['id']).first()
            if not relation_exist:
                asset_vul_relations.append(IastVulAssetRelation(asset_vul_id=asset_vul.id, asset_id=asset_vl['id'],
                                                                create_time=timestamp, status_id=1))

    if asset_vul_relations:
        IastVulAssetRelation.objects.bulk_create(asset_vul_relations)
        if ELASTICSEARCH_STATE:
            asset_vul_created = IastVulAssetRelation.objects.filter(
                asset_vul=asset_vul, create_time=timestamp, status_id=1).all()
            IastAssetVulnerabilityDocument().update(asset_vul_created)

def update_asset_aggr(asset):
    try:
        project_count = 0
        asset_aggr = AssetAggr.objects.filter(signature_value=asset.signature_value, version=asset.version).first()
        project_count_query = Asset.objects.filter(project_id__gt=0, signature_value=asset.signature_value,
                                                   version=asset.version).values(
            'signature_value', 'version').annotate(project_count=Count('project_id', distinct=True))
        if project_count_query:
            project_count = [_['project_count'] for _ in project_count_query][0]

        if asset_aggr:
            asset_aggr.version = asset.version
            asset_aggr.safe_version = asset.safe_version
            asset_aggr.last_version = asset.last_version
            asset_aggr.level = asset.level
            asset_aggr.vul_count = asset.vul_count
            asset_aggr.vul_critical_count = asset.vul_critical_count
            asset_aggr.vul_high_count = asset.vul_high_count
            asset_aggr.vul_medium_count = asset.vul_medium_count
            asset_aggr.vul_low_count = asset.vul_low_count
            asset_aggr.vul_info_count = asset.vul_info_count
            asset_aggr.language = asset.language
            asset_aggr.license = asset.license
            asset_aggr.is_del = asset.is_del
            asset_aggr.project_count = project_count
            asset_aggr.save()
        else:
            AssetAggr.objects.create(
                package_name=asset.package_name,
                signature_value=asset.signature_value,
                version=asset.version,
                safe_version=asset.safe_version,
                last_version=asset.last_version,
                level=asset.level,
                vul_count=asset.vul_count,
                vul_critical_count=asset.vul_critical_count,
                vul_high_count=asset.vul_high_count,
                vul_medium_count=asset.vul_medium_count,
                vul_low_count=asset.vul_low_count,
                project_count=project_count,
                language=asset.language,
                license=asset.license,
                is_del=asset.is_del)
    except Exception as e:
        logger.error("update_asset_aggr error {}:".format(e))


def get_asset_id_by_aggr_id(aggr_id, asset_ids=None):
    data_ids = []
    asset_aggr = AssetAggr.objects.filter(id=aggr_id).first()
    if asset_aggr:
        assets = Asset.objects.filter(signature_value=asset_aggr.signature_value, version=asset_aggr.version)
        if asset_ids:
            assets = assets.filter(id__in=asset_ids)
        asset_datas = assets.values('id').all()
        for asset in asset_datas:
            data_ids.append(asset['id'])

    return data_ids


def get_package_name_by_aql(aql):
    name = ''

    if aql:
        aql_split = aql.split(':')
        if len(aql_split) > 0:
            del aql_split[-2]
            del aql_split[-1]
            del aql_split[0]
            name = ':'.join(aql_split)

    return name
