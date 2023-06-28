#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from elasticsearch_dsl import Q, Search
from dongtai_common.models.asset import IastAssetDocument
from dongtai_web.aggregation.aggregation_common import auth_user_list_str
from dongtai_common.models.asset_aggr import AssetAggrDocument
from dongtai_conf.settings import ELASTICSEARCH_STATE
from dongtai_common.common.utils import make_hash
from dongtai_conf import settings
from django.core.cache import cache
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.models.project import IastProject
from dongtai_common.models.program_language import IastProgramLanguage
from dongtai_common.models.vulnerablity import IastVulnerabilityStatus
from dongtai_common.models.strategy import IastStrategyModel
from elasticsearch_dsl import A
from elasticsearch import Elasticsearch
import logging

import pymysql
from django.db import connection

from dongtai_common.endpoint import R, UserEndPoint

from dongtai_common.models.asset_aggr import AssetAggr

from dongtai_web.base.project_version import get_project_version, get_project_version_by_id
from dongtai_web.serializers.sca import ScaAssetSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from dongtai_common.models.asset import Asset
from itertools import chain

WINDOW_SIZE = 5

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
    else:
        order = 'vul_count'
        order_type = 'desc'

    return order, order_type


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


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
        description=_("use the specified project information to obtain the corresponding component."
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
        departments = request.user.get_relative_department()
        department_ids = [department.id for department in departments]
        base_query_sql = " LEFT JOIN iast_asset ON iast_asset.signature_value = iast_asset_aggr.signature_value WHERE  iast_asset.department_id in %s and iast_asset.is_del=0 "
        list_sql_params = [auth_user_ids]
        count_sql_params = [auth_user_ids]
        es_query = {}
        es_query['page_size'] = page_size
        es_query['page'] = page
        es_query['user_id'] = request.user.id
        asset_aggr_where = " and iast_asset_aggr.id>0 "
        where_conditions = []
        where_conditions_dict = {}
        #user_ids = [_i.id for _i in auth_users]
        if len(department_ids) == 1:
            where_conditions.append('department_id = %(department_ids)s')
            where_conditions_dict['department_ids'] = department_ids[0]
        else:
            where_conditions.append('department_id IN %(department_ids)s')
            where_conditions_dict['department_ids'] = department_ids

        project_id = request_data.get('project_id', None)
        if project_id and project_id != '':
            es_query['bind_project_id'] = project_id
            version_id = request.GET.get('version_id', None)
            if not version_id:
                current_project_version = get_project_version(
                    project_id)
            else:
                current_project_version = get_project_version_by_id(version_id)

            base_query_sql = base_query_sql + " and iast_asset.project_id=%s and iast_asset.project_version_id=%s "
            project_version_id = current_project_version.get("version_id", 0)
            es_query['project_version_id'] = project_version_id
            list_sql_params.append(project_id)
            count_sql_params.append(project_id)
            list_sql_params.append(project_version_id)
            count_sql_params.append(project_version_id)
            where_conditions.append('project_id = %(project_id)s ')
            where_conditions_dict['project_id'] = project_id
            where_conditions.append(
                'project_version_id = %(project_version_id)s')
            where_conditions_dict['project_version_id'] = project_version_id

        total_count_sql = "SELECT count(distinct(iast_asset_aggr.id)) as alltotal FROM iast_asset_aggr {base_query_sql} {where_sql} limit 1 "
        list_query_sql = "SELECT iast_asset_aggr.signature_value FROM iast_asset_aggr {base_query_sql} {where_sql} GROUP BY iast_asset_aggr.id {order_sql} {page_sql} "

        language = request_data.get('language', None)
        if language:
            asset_aggr_where = asset_aggr_where + " and iast_asset_aggr.language in %s"
            count_sql_params.append(language)
            list_sql_params.append(language)
            es_query['languages'] = language
            if len(language) == 1:
                where_conditions.append('language = %(languages)s')
                where_conditions_dict['languages'] = language[0]
            else:
                where_conditions.append('language IN %(languages)s')
                where_conditions_dict['languages'] = language
        asset_aggr_where, count_sql_params, list_sql_params = self.extend_sql(
            request_data, asset_aggr_where, count_sql_params, list_sql_params)

        level_ids = request_data.get('level_id', None)
        if level_ids:
            es_query['level_ids'] = level_ids
            level_ids = [str(x) for x in level_ids]
            asset_aggr_where = asset_aggr_where + " and iast_asset_aggr.level_id in %s"
            count_sql_params.append(level_ids)
            list_sql_params.append(level_ids)
            if len(level_ids) == 1:
                where_conditions.append('level_id = %(level_ids)s')
                where_conditions_dict['level_ids'] = level_ids[0]
            else:
                where_conditions.append('level_id IN %(level_ids)s')
                where_conditions_dict['level_ids'] = level_ids

        package_kw = request_data.get('keyword', None)
        if package_kw:
            es_query['search_keyword'] = package_kw

    #     package_kw = pymysql.converters.escape_string(package_kw)
        if package_kw and package_kw.strip() != '':
            package_kw = '%{}%'.format(package_kw)
            asset_aggr_where = asset_aggr_where + " and iast_asset_aggr.package_name like %s "
            list_sql_params.append(package_kw)
            count_sql_params.append(package_kw)
            where_conditions.append('package_name LIKE %(package_kw)s')
            where_conditions_dict['package_kw'] = package_kw

        license = request_data.get('license', None)
        if license:
            es_query['license'] = license

        if license:
            list_sql_params.append(license)
            count_sql_params.append(license)
            where_conditions.append('license IN %(license)s')
            where_conditions_dict['license'] = license

        order_by = '-vul_count'
        order = request.data.get('order', None)
        if not order or order == "-":
            order = '-vul_count'

        order_fields = ['level', 'license', 'vul_count', 'project_count']
        order, order_type = get_order_params(order_fields, order)
        es_query['order'] = order
        es_query['order_type'] = order_type
        #        if ELASTICSEARCH_STATE:
        #            data = get_vul_list_from_elastic_searchv2(**es_query)
        #        else:
        data = mysql_search(where_conditions, where_conditions_dict, page_size,
                            order_type, order, page)
        query_data = ScaAssetSerializer(data, many=True).data

        return R.success(data=query_data)
#        order_sql = " order by {} {},iast_asset_aggr.id DESC ".format(
#            order, order_type)
#        page_sql = " limit %s,%s"
#        list_sql_params.append(query_start)
#        list_sql_params.append(page_size)
#
#        total_count_sql = total_count_sql.format(base_query_sql=base_query_sql,
#                                                 where_sql=asset_aggr_where)
#        list_query_sql = list_query_sql.format(base_query_sql=base_query_sql,
#                                               where_sql=asset_aggr_where,
#                                               order_sql=order_sql,
#                                               page_sql=page_sql)
#
#        total_count = 0
#        sca_ids = []
#        try:
#            with connection.cursor() as cursor:
#                cursor.execute(total_count_sql, count_sql_params)
#                total_count_query = cursor.fetchone()
#                total_count = total_count_query[0]
#
#            with connection.cursor() as cursor:
#                cursor.execute(list_query_sql, list_sql_params)
#                list_query = cursor.fetchall()
#                if list_query:
#                    for _l in list_query:
#                        sca_ids.append(_l[0])
#        except Exception as e:
#            logger.warning("sca list error:{}".format(e))
#
#
#        if ELASTICSEARCH_STATE :
#            query_data = ScaAssetSerializer(get_vul_list_from_elastic_search(
#                sca_ids, order_by),
#                                            many=True).data
#        else:
#        query_data = ScaAssetSerializer(
#            AssetAggr.objects.filter(signature_value__in=sca_ids).order_by(
#                order_by).select_related('level'),
#            many=True).data
#
#        return R.success(data=query_data)

    def extend_sql(self, request_data, asset_aggr_where, count_sql_params,
                   list_sql_params):
        return asset_aggr_where, count_sql_params, list_sql_params


def get_vul_list_from_elastic_search(sca_ids=[], order=None):
    must_query = [
        Q('terms', **{"signature_value": sca_ids}),
    ]
    a = Q('bool', must=must_query)
    extra_dict = {}
    order_list = []
    if order:
        order_list.insert(0, order)
    res = AssetAggrDocument.search().query(a).extra(**extra_dict).sort(
        *order_list)[:len(sca_ids)]
    resp = res.execute()
    vuls = [i._d_ for i in list(resp)]
    for i in vuls:
        if '@timestamp' in i.keys():
            del i['@timestamp']
    res_vul = [AssetAggr(**i) for i in vuls]
    return res_vul


def get_vul_list_from_elastic_searchv2(user_id,
                                       bind_project_id=None,
                                       project_version_id=None,
                                       level_ids=[],
                                       languages=[],
                                       order="",
                                       order_type="",
                                       page=1,
                                       page_size=10,
                                       search_keyword="",
                                       extend_filter={}):
    user_id_list = [user_id]
    auth_user_info = auth_user_list_str(user_id=user_id)
    user_id_list = auth_user_info['user_list']
    must_query = [
        Q('terms', user_id=user_id_list),
        Q('terms', is_del=[0]),
    ]
    order_list: list[str | dict] = ['-signature_value.keyword']
    if order:
        order_list.insert(0, {order: {'order': order_type}})
    if bind_project_id:
        must_query.append(Q('terms', project_id=[int(bind_project_id)]))
    if project_version_id:
        must_query.append(Q('terms', project_version_id=[project_version_id]))
    if languages:
        must_query.append(Q('terms', **{"language.keyword": languages}))
    if level_ids:
        must_query.append(Q('terms', level_id=level_ids))
    if search_keyword:
        must_query.append(
            Q("wildcard",
              **{"package_name.keyword": {
                  "value": f"*{search_keyword}*"
              }}))
    hashkey = f"{__name__}_es" + str(
        make_hash([
            user_id, level_ids, languages, search_keyword, page_size,
            bind_project_id, project_version_id
        ]))
    after_table = cache.get(hashkey, {})
    after_key = after_table.get(page, None)
    if page != 1 and not after_key:
        return []
    extra_dict = {'collapse': {'field': 'signature_value.keyword'}}
    after_fields = []
    for info in order_list:
        field = ''
        if isinstance(info, dict):
            field = list(info.keys())[0]
        if isinstance(info, str):
            if info.startswith('-'):
                field = info[1::]
            else:
                field = info
        if field == 'package_name.keyword':
            field = 'package_name'
        after_fields.append(field)
    if after_key:
        # sub_after_must_query = []
        sub_after_must_not_query = []
        # sub_after_should_query = []
        sub_after_must_not_query.append(
            Q('terms', **{"signature_value.keyword": after_key}))
        # for info, value in zip(order_list, after_key):
        #    field = ''
        #    opt = ''
        #    if isinstance(info, dict):
        #        field = list(info.keys())[0]
        #        if info[field]['order'] == 'desc':
        #            opt = 'lte'
        #        else:
        #            opt = 'gte'
        #    if isinstance(info, str):
        #        if info.startswith('-'):
        #            field = info[1::]
        #            opt = 'lt'
        #        else:
        #            field = info
        #            opt = 'gt'
        #    sub_after_must_query.append(Q('range', **{field: {opt: value}}))
        must_query.append(
            Q(
                'bool',
                must_not=sub_after_must_not_query,
                # must=sub_after_must_query,
                # should=sub_after_should_query,
                # minimum_should_match=1
            ))
    a = Q('bool', must=must_query)
    search = IastAssetDocument.search().query(
        Q('bool',
          must=must_query)).extra(**extra_dict).sort(*order_list)[:page_size *
                                                                  WINDOW_SIZE]
    logger.debug(f"search_query : {search.to_dict()}")
    resp = search.execute()
    vuls = [i._d_ for i in list(resp)]
    if not after_key:
        after_key = []
    for i in range(WINDOW_SIZE):
        chunk = vuls[page_size * i:page_size * (i + 1)]
        if len(chunk) != page_size:
            break
        new_after_key = after_key.copy()
        new_after_key.extend([i['signature_value'] for i in chunk])
        # latest_data = chunk[-1]
        # after_key = [
        #    latest_data.get(after_field) for after_field in after_fields
        # ]
        after_table[page + i + 1] = new_after_key
        after_key = new_after_key
    for i in vuls:
        if '@timestamp' in i.keys():
            del i['@timestamp']
        if 'signature_value.keyword' in i.keys():
            del i['signature_value.keyword']
    res_vul = [Asset(**i) for i in vuls]
    # if resp.hits:
    #    afterkey = resp.hits[-1].meta['sort']
    #    after_table[page + 1] = afterkey
    print(after_table)
    cache.set(hashkey, after_table)
    return res_vul[:page_size]


def mysql_search(where_conditions, where_conditions_dict, page_size,
                 order_type, order, page):
    hashkey = f"{__name__}_mysql" + str(
        make_hash([
            where_conditions, where_conditions_dict, page_size, order_type,
            order
        ]))
    after_table = cache.get(hashkey, {})
    after_key = after_table.get(page, None)
    if page != 1 and not after_key:
        return []
    if after_key:
        after_order_value, after_signature = after_key
        if order_type == 'desc':
            where_conditions.append(
                f"({order}, signature_value) < %(after_order_value)s ")
            where_conditions_dict['after_order_value'] = (after_order_value,
                                                          after_signature)
        else:
            where_conditions.append(
                f"({order}, signature_value) > %(after_order_value)s ")
            where_conditions_dict['after_order_value'] = (after_order_value,
                                                          after_signature)


#        where_conditions.append(f"signature_value < %(after_order_id)s ")
#        where_conditions_dict['after_order_id'] = after_signature

    order_conditions = [
        "signature_value DESC",
    ]
    order_conditions_dict = {
        #        "id": 'id',
    }
    if order_type == 'desc':
        order_conditions.insert(0, f"{order} DESC")
    else:
        order_conditions.insert(0, f"{order} ASC")
    order_conditions_dict["field"] = order
    final_sql = """SELECT ia2.* FROM iast_asset ia2
        RIGHT JOIN
        (SELECT MAX(id) as _2 FROM iast_asset ia
        WHERE {where_place}
        GROUP BY signature_value
        ) AS TMP ON ia2.id = TMP._2
        ORDER BY {order_place} LIMIT {size} ;""".format(
        where_place=' AND '.join(where_conditions)
        if where_conditions else '1 = 1',
        order_place=' , '.join(order_conditions)
        if order_conditions else 'NULL',
        size='%(size)s')
    base_dict = {'size': page_size * WINDOW_SIZE}
    # base_dict.update(order_conditions_dict)
    base_dict.update(where_conditions_dict)
    data = Asset.objects.raw(final_sql, params=base_dict)
    data = list(data)
    for i in range(WINDOW_SIZE):
        chunk = data[page_size * i:page_size * (i + 1)]
        if len(chunk) != page_size:
            break
        latest_data = chunk[-1]
        after_key = [
            getattr(latest_data, order),
            getattr(latest_data, 'signature_value')
        ]
        after_table[page + i + 1] = after_key
    cache.set(hashkey, after_table)
    return data[:page_size]
