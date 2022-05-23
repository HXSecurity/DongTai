#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging

import pymysql
from django.db import connection
from dongtai.endpoint import R, UserEndPoint

from dongtai.models.asset_aggr import AssetAggr

from iast.base.project_version import get_project_version, get_project_version_by_id
from iast.serializers.sca import ScaAssetSerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy

logger = logging.getLogger(__name__)
_ResponseSerializer = get_response_serializer(ScaAssetSerializer(many=True))


def get_order_params(order_fields, order_by):
    order_type = 'asc'

    if '-' in order_by:
        order_by = order_by.split('-')[1]
        order_type = 'desc'

    if order_by and order_by in order_fields:
        if order_by == 'level':
            order_by = "{}_id".format(order_by)
            if order_type == 'asc':
                order_type = 'desc'
            else:
                order_type = 'asc'
    order = order_by
    order = "iast_asset_aggr.{}".format(order)
    return order, order_type


class ScaList(UserEndPoint):
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
                'name': "level",
                'type': int,
                'description': _('The id of level of vulnerability'),
            },
            {
                'name': "project_id",
                'type': int,
                'description': _('Id of Project'),
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
                    "status":
                        201,
                    "msg":
                        "success",
                    "data": [
                        {
                            "id": 13293,
                            "package_name": "message-business-7.1.0.Final.jar",
                            "version": "7.1.0.Final",
                            "project_name": "No application",
                            "project_id": 0,
                            "project_version": "No application version",
                            "language": "JAVA",
                            "agent_name":
                                "Mac OS X-bogon-v1.0.0-0c864ba2a60b48aaa1a8b49a53a6749b",
                            "signature_value":
                                "f744df92326c4bea7682fd16004bec184148db07",
                            "level": "INFO",
                            "level_type": 4,
                            "vul_count": 0,
                            "dt": 1631189450
                        }
                    ],
                    "page": {
                        "alltotal": 795,
                        "num_pages": 795,
                        "page_size": 1
                    }
                }
            }
        ],
        tags=[_('Component')],
        summary=_("Component List (with project)"),
        description=
        _("use the specified project information to obtain the corresponding component."
          ),
        response_schema=_ResponseSerializer)
    def post(self, request):
        """
        :param request:
        :return:
        """
        auth_users = self.get_auth_users(request.user)
        request_data = request.data
        page = request_data.get('page', 1)
        page_size = request_data.get('pageSize', 20)

        page_size = min(50, int(page_size))

        query_start = (page - 1) * page_size

        auth_user_ids = [str(_i.id) for _i in auth_users]
        auth_user_ids_str = ','.join(auth_user_ids)

        base_query_sql = " LEFT JOIN iast_asset ON iast_asset.signature_value = iast_asset_aggr.signature_value WHERE iast_asset.user_id in ({}) and iast_asset.is_del=0 ".format(
            auth_user_ids_str)
        order_by = '-vul_count'
        order = request.data.get('order', None)
        if not order or order == "-":
            order = '-vul_count'
        else:
            order_by = order
        order_fields = [
            'level', 'license', 'vul_count', 'project_count'
        ]

        order, order_type = get_order_params(order_fields, order)

        order_sql = " order by {} {},iast_asset_aggr.id DESC  ".format(order, order_type)
        page_sql = " limit {},{}".format(query_start, page_size)

        asset_aggr_where = " and iast_asset_aggr.id>0 "

        project_id = request_data.get('project_id', None)
        if project_id and project_id != '':

            version_id = request.GET.get('version_id', None)
            if not version_id:
                current_project_version = get_project_version(project_id, auth_users)
            else:
                current_project_version = get_project_version_by_id(version_id)

            base_query_sql = base_query_sql + " and iast_asset.project_id={} and iast_asset.project_version_id= {}".format(
                project_id, current_project_version.get("version_id", 0))
        total_count_sql = "SELECT count(distinct(iast_asset_aggr.id)) as alltotal FROM iast_asset_aggr {base_query_sql} {where_sql} limit 1 "
        list_query_sql = "SELECT iast_asset_aggr.id FROM iast_asset_aggr {base_query_sql} {where_sql} GROUP BY iast_asset_aggr.id {order_sql} {page_sql} "

        language = request_data.get('language', None)
        if language:
            asset_aggr_where = asset_aggr_where + " and iast_asset_aggr.language in ({})".format(
                "'" + "','".join(language) + "'")
        license = request_data.get('license', None)
        if license:
            if '未知' in license:
                license.append("""""")
            asset_aggr_where = asset_aggr_where + " and iast_asset_aggr.license in ({})".format(
                "'" + "','".join(license) + "'")

        level_ids = request_data.get('level_id', None)
        if level_ids:
            level_ids = [str(x) for x in level_ids]
            asset_aggr_where = asset_aggr_where + " and iast_asset_aggr.level_id in ({})".format(','.join(level_ids))

        package_kw = request_data.get('keyword', None)
        if package_kw:
            package_kw = pymysql.converters.escape_string(package_kw)
        if package_kw and package_kw.strip() != '':
            package_kw = '%%{}%%'.format(package_kw)
            asset_aggr_where = asset_aggr_where + " and iast_asset_aggr.package_name like %s "

        total_count_sql = total_count_sql.format(base_query_sql=base_query_sql, where_sql=asset_aggr_where)
        list_query_sql = list_query_sql.format(base_query_sql=base_query_sql, where_sql=asset_aggr_where,
                                               order_sql=order_sql, page_sql=page_sql)

        total_count = 0
        sca_ids = []
        try:
            with connection.cursor() as cursor:
                # 漏洞等级汇总
                if package_kw:
                    cursor.execute(total_count_sql, [package_kw])
                else:
                    cursor.execute(total_count_sql)
                total_count_query = cursor.fetchone()
                if total_count_query:
                    total_count = total_count_query[0]
                if package_kw:
                    cursor.execute(list_query_sql, [package_kw])
                else:
                    cursor.execute(list_query_sql)
                page_data = cursor.fetchall()
                if page_data:
                    sca_ids = [i[0] for i in page_data]
        except Exception as e:
            logger.warning("sca list error:{}".format(e))

        page_summary = {
            "alltotal": total_count,
            "page_size": page_size,
            "order": order,
            "order_type": order_type
        }
        query_data = ScaAssetSerializer(
            AssetAggr.objects.filter(pk__in=sca_ids).order_by(order_by).select_related('level'),
            many=True).data

        return R.success(data=query_data, page=page_summary)
