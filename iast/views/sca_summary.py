#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import pymysql
from dongtai.endpoint import R, UserEndPoint
from dongtai.models.vul_level import IastVulLevel
from django.db import connection
from iast.base.agent import get_project_vul_count, get_agent_languages, initlanguage
from iast.base.project_version import get_project_version, get_project_version_by_id
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from iast.serializers.vul import VulSummaryTypeSerializer, VulSummaryProjectSerializer, VulSummaryLevelSerializer, \
    VulSummaryLanguageSerializer
from rest_framework import serializers


class _ScaSummaryResponseDataSerializer(serializers.Serializer):
    language = VulSummaryLanguageSerializer(many=True)
    level = VulSummaryLevelSerializer(many=True)
    projects = VulSummaryProjectSerializer(many=True)


_ResponseSerializer = get_response_serializer(
    _ScaSummaryResponseDataSerializer())


class ScaSummary(UserEndPoint):
    name = "rest-api-sca-summary"
    description = _("Three-party components overview")

    @extend_schema_with_envcheck(
        [
            {
                'name': "page",
                'type': int,
                'default': 1,
                'required': False,
                'description': _('Page index'),
            },
            {
                'name': "pageSize",
                'type': int,
                'default': 20,
                'required': False,
                'description': _('Number per page'),
            },
            {
                'name': "language",
                'type': str,
                'description': _("programming language"),
            },
            {
                'name': "project_name",
                'type': str,
                'deprecated': True,
                'description': _('Name of Project'),
            },
            {
                'name': "project_id",
                'type': int,
                'description': _('Id of Project'),
            },
            {
                'name': "level",
                'type': int,
                'description': _('The id level of vulnerability'),
            },
            {
                'name':
                    "version_id",
                'type':
                    int,
                'description':
                    _("The default is the current version id of the project.")
            },
            {
                'name': "keyword",
                'type': str,
                'description':
                    _("Fuzzy keyword search field for package_name.")
            },
            {
                'name':
                    "order",
                'type':
                    str,
                'description':
                    format_lazy(
                        "{} : {}", _('Sorted index'), ",".join([
                            'version', 'level', 'vul_count', 'language',
                            'package_name'
                        ]))
            },
        ], [], [
            {
                'name':
                    _('Get data sample'),
                'description':
                    _("The aggregation results are programming language, risk level, vulnerability type, project"
                      ),
                'value': {
                    "status": 201,
                    "msg": "success",
                    "data": {
                        "language": [
                            {
                                "language": "JAVA",
                                "count": 17
                            }, {
                                "language": "PYTHON",
                                "count": 0
                            }
                        ],
                        "level": [
                            {
                                "level": "HIGH",
                                "count": 0,
                                "level_id": 1
                            }, {
                                "level": "MEDIUM",
                                "count": 0,
                                "level_id": 2
                            }, {
                                "level": "LOW",
                                "count": 0,
                                "level_id": 3
                            }, {
                                "level": "INFO",
                                "count": 17,
                                "level_id": 4
                            }
                        ],
                        "projects": [
                            {
                                "project_name": "demo",
                                "count": 17,
                                "id": 67
                            }
                        ]
                    }
                }
            }
        ],
        tags=[_('Component')],
        summary=_("Component Summary (with project)"),
        description=
        _("Use the specified project information to get the corresponding component summary"
          ),
        response_schema=_ResponseSerializer)
    def post(self, request):
        """
        :param request:
        :return:
        """

        end = {
            "status": 201,
            "msg": "success",
            "data": {}
        }

        auth_users = self.get_auth_users(request.user)
        request_data = request.data

        auth_user_ids = [str(_i.id) for _i in auth_users]
        auth_user_ids_str = ','.join(auth_user_ids)
        base_query_sql = " LEFT JOIN iast_asset ON iast_asset.signature_value = iast_asset_aggr.signature_value WHERE iast_asset.user_id in ({}) and iast_asset.is_del=0 ".format(
            auth_user_ids_str)
        asset_aggr_where = " and iast_asset_aggr.is_del=0 "
        package_kw = request_data.get('keyword', "")
        if package_kw:
            package_kw = pymysql.converters.escape_string(package_kw)

        if package_kw and package_kw.strip() != '':
            package_kw = '%%{}%%'.format(package_kw)
            asset_aggr_where = asset_aggr_where + " and iast_asset_aggr.package_name like %s"

        project_id = request_data.get('project_id', None)
        if project_id and project_id != '':
            version_id = request.GET.get('version_id', None)
            if not version_id:
                current_project_version = get_project_version(project_id, auth_users)
            else:
                current_project_version = get_project_version_by_id(version_id)
            base_query_sql = base_query_sql + " and iast_asset.project_id={} and iast_asset.project_version_id= {}".format(
                project_id, current_project_version.get("version_id", 0))

        levelInfo = IastVulLevel.objects.filter(id__lt=5).all()
        levelNameArr = {}
        levelIdArr = {}
        DEFAULT_LEVEL = {}
        if levelInfo:
            for level_item in levelInfo:
                DEFAULT_LEVEL[level_item.name_value] = 0
                levelNameArr[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value

        _temp_data = dict()
        with connection.cursor() as cursor:
            # 漏洞等级汇总
            level_summary_sql = "SELECT iast_asset_aggr.level_id,count(DISTINCT(iast_asset_aggr.id)) as total FROM iast_asset_aggr {base_query_sql} {where_sql} GROUP BY iast_asset_aggr.level_id "
            level_summary_sql = level_summary_sql.format(base_query_sql=base_query_sql, where_sql=asset_aggr_where)
            if package_kw:
                cursor.execute(level_summary_sql, [package_kw])
            else:
                cursor.execute(level_summary_sql)
            level_summary = cursor.fetchall()
            if level_summary:
                for item in level_summary:
                    level_id, total = item
                    _temp_data[levelIdArr[level_id]] = total

        DEFAULT_LEVEL.update(_temp_data)
        end['data']['level'] = [{
            'level': _key, 'count': _value, 'level_id': levelNameArr[_key]
        } for _key, _value in DEFAULT_LEVEL.items()]
        default_language = initlanguage()
        language_summary_sql = "SELECT iast_asset_aggr.language,count(DISTINCT(iast_asset_aggr.id)) as total FROM iast_asset_aggr {base_query_sql} {where_sql} GROUP BY iast_asset_aggr.language "
        language_summary_sql = language_summary_sql.format(base_query_sql=base_query_sql, where_sql=asset_aggr_where)
        with connection.cursor() as cursor:
            # 漏洞语言汇总

            if package_kw:
                cursor.execute(language_summary_sql, [package_kw])
            else:
                cursor.execute(language_summary_sql)
            language_summary = cursor.fetchall()
            if language_summary:
                for _l in language_summary:
                    language, total = _l
                    if default_language.get(language, None):
                        default_language[language] = total + default_language[language]
                    else:
                        default_language[language] = total

        end['data']['language'] = [{
            'language': _key, 'count': _value
        } for _key, _value in default_language.items()]

        default_license = dict()
        license_summary_sql = "SELECT iast_asset_aggr.license,count(DISTINCT(iast_asset_aggr.id)) as total FROM iast_asset_aggr {base_query_sql} {where_sql} GROUP BY iast_asset_aggr.license "
        license_summary_sql = license_summary_sql.format(base_query_sql=base_query_sql, where_sql=asset_aggr_where)
        with connection.cursor() as cursor:
            # 漏洞license汇总
            if package_kw:
                cursor.execute(license_summary_sql, [package_kw])
            else:
                cursor.execute(license_summary_sql)
            license_summary = cursor.fetchall()
            if license_summary:
                for _l in license_summary:
                    license, total = _l
                    if default_license.get(license, None):
                        default_license[license] = total + default_license[license]
                    else:
                        default_license[license] = total

        end['data']['license'] = [{
            'license': _key, 'count': _value
        } for _key, _value in default_license.items() if _key]
        if '' in default_license:
            end['data']['license'].append({'license': '未知', 'count': default_license['']})

        return R.success(data=end['data'])
