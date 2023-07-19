#!/usr/bin/env python
import pymysql
from django.db import connection
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from elasticsearch import Elasticsearch
from elasticsearch_dsl import A, Q
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models import LANGUAGE_DICT
from dongtai_common.models.asset import IastAssetDocument
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_conf import settings
from dongtai_web.aggregation.aggregation_common import auth_user_list_str
from dongtai_web.base.agent import initlanguage
from dongtai_web.base.project_version import (
    get_project_version,
    get_project_version_by_id,
)
from dongtai_web.serializers.vul import (
    VulSummaryLanguageSerializer,
    VulSummaryLevelSerializer,
    VulSummaryProjectSerializer,
)
from dongtai_web.utils import dict_transfrom, extend_schema_with_envcheck, get_response_serializer


class _ScaSummaryResponseDataSerializer(serializers.Serializer):
    language = VulSummaryLanguageSerializer(many=True)
    level = VulSummaryLevelSerializer(many=True)
    projects = VulSummaryProjectSerializer(many=True)


_ResponseSerializer = get_response_serializer(_ScaSummaryResponseDataSerializer())


class ScaSummary(UserEndPoint):
    name = "rest-api-dongtai_sca-summary"
    description = _("Three-party components overview")

    @extend_schema_with_envcheck(
        [
            {
                "name": "page",
                "type": int,
                "default": 1,
                "required": False,
                "description": _("Page index"),
            },
            {
                "name": "pageSize",
                "type": int,
                "default": 20,
                "required": False,
                "description": _("Number per page"),
            },
            {
                "name": "language",
                "type": str,
                "description": _("programming language"),
            },
            {
                "name": "project_name",
                "type": str,
                "deprecated": True,
                "description": _("Name of Project"),
            },
            {
                "name": "project_id",
                "type": int,
                "description": _("Id of Project"),
            },
            {
                "name": "level",
                "type": int,
                "description": _("The id level of vulnerability"),
            },
            {
                "name": "version_id",
                "type": int,
                "description": _(
                    "The default is the current version id of the project."
                ),
            },
            {
                "name": "keyword",
                "type": str,
                "description": _("Fuzzy keyword search field for package_name."),
            },
            {
                "name": "order",
                "type": str,
                "description": format_lazy(
                    "{} : {}",
                    _("Sorted index"),
                    "version,level,vul_count,language,package_name",
                ),
            },
        ],
        [],
        [
            {
                "name": _("Get data sample"),
                "description": _(
                    "The aggregation results are programming language, risk level, vulnerability type, project"
                ),
                "value": {
                    "status": 201,
                    "msg": "success",
                    "data": {
                        "language": [
                            {"language": "JAVA", "count": 17},
                            {"language": "PYTHON", "count": 0},
                        ],
                        "level": [
                            {"level": "HIGH", "count": 0, "level_id": 1},
                            {"level": "MEDIUM", "count": 0, "level_id": 2},
                            {"level": "LOW", "count": 0, "level_id": 3},
                            {"level": "INFO", "count": 17, "level_id": 4},
                        ],
                        "projects": [{"project_name": "demo", "count": 17, "id": 67}],
                    },
                },
            }
        ],
        tags=[_("Component")],
        summary=_("Component Summary (with project)"),
        description=_(
            "Use the specified project information to get the corresponding component summary"
        ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        """
        :param request:
        :return:
        """

        end = {"status": 201, "msg": "success", "data": {}}

        request_data = request.data

        departments = request.user.get_relative_department()
        department_ids = [i.id for i in departments]
        base_query_sql = "WHERE iast_asset.department_id in %s and iast_asset.is_del=0 "
        sql_params = [department_ids]
        asset_aggr_where = " and iast_asset.is_del=0 "
        package_kw = request_data.get("keyword", "")
        es_query = {}
        if package_kw:
            es_query["search_keyword"] = package_kw
            package_kw = pymysql.converters.escape_string(package_kw)

        if package_kw and package_kw.strip() != "":
            package_kw = f"%%{package_kw}%%"
            asset_aggr_where = asset_aggr_where + " and iast_asset.package_name like %s"
            sql_params.append(package_kw)
        project_id = request_data.get("project_id", None)
        if project_id and project_id != "":
            version_id = request.GET.get("version_id", None)
            current_project_version = get_project_version(project_id) if not version_id else get_project_version_by_id(version_id)
            asset_aggr_where = (
                asset_aggr_where
                + " and iast_asset.project_id=%s and iast_asset.project_version_id=%s "
            )
            sql_params.append(project_id)
            sql_params.append(current_project_version.get("version_id", 0))
            es_query["bind_project_id"] = project_id
            es_query["project_version_id"] = current_project_version.get(
                "version_id", 0
            )

        #        if ELASTICSEARCH_STATE:
        #
        levelInfo = IastVulLevel.objects.filter(id__lt=5).all()
        levelNameArr = {}
        levelIdArr = {}
        DEFAULT_LEVEL = {}
        if levelInfo:
            for level_item in levelInfo:
                DEFAULT_LEVEL[level_item.name_value] = 0
                levelNameArr[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value

        _temp_data = {}
        # 漏洞等级汇总
        level_summary_sql = "SELECT iast_asset.level_id,count(DISTINCT(iast_asset.signature_value)) as total FROM iast_asset {base_query_sql} {where_sql} GROUP BY iast_asset.level_id "
        level_summary_sql = level_summary_sql.format(
            base_query_sql=base_query_sql, where_sql=asset_aggr_where
        )

        with connection.cursor() as cursor:
            cursor.execute(level_summary_sql, sql_params)
            level_summary = cursor.fetchall()
            if level_summary:
                for item in level_summary:
                    level_id, total = item
                    _temp_data[levelIdArr[level_id]] = total

        DEFAULT_LEVEL.update(_temp_data)
        end["data"]["level"] = [
            {"level": _key, "count": _value, "level_id": levelNameArr[_key]}
            for _key, _value in DEFAULT_LEVEL.items()
        ]

        default_language = initlanguage()
        language_summary_sql = "SELECT iast_asset.language,count(DISTINCT(iast_asset.signature_value)) as total FROM iast_asset {base_query_sql} {where_sql} GROUP BY iast_asset.language "
        language_summary_sql = language_summary_sql.format(
            base_query_sql=base_query_sql, where_sql=asset_aggr_where
        )

        with connection.cursor() as cursor:
            cursor.execute(language_summary_sql, sql_params)
            language_summary = cursor.fetchall()
            if language_summary:
                for _l in language_summary:
                    language, total = _l
                    if default_language.get(language, None):
                        default_language[language] = total + default_language[language]
                    else:
                        default_language[language] = total

        end["data"]["language"] = [
            {"language": _key, "count": _value}
            for _key, _value in default_language.items()
        ]

        end, base_query_sql, asset_aggr_where, sql_param = self.get_extend_data(
            end, base_query_sql, asset_aggr_where, sql_params
        )

        return R.success(data=end["data"])

    def get_extend_data(
        self, end: dict, base_query_sql: str, asset_aggr_where: str, sql_params: list
    ):
        return end, base_query_sql, asset_aggr_where, sql_params

    def get_data_from_es(self, user_id, es_query):
        resp, origin_resp = get_vul_list_from_elastic_search(user_id, **es_query)
        return resp, origin_resp


def get_vul_list_from_elastic_search(
    user_id,
    bind_project_id=None,
    project_version_id=None,
    search_keyword="",
    extend_aggs_buckets={},
):
    user_id_list = [user_id]
    auth_user_info = auth_user_list_str(user_id=user_id)
    user_id_list = auth_user_info["user_list"]
    must_query = [
        Q("terms", user_id=user_id_list),
        Q("terms", is_del=[0]),
    ]
    if bind_project_id:
        must_query.append(Q("terms", project_id=[bind_project_id]))
    if project_version_id:
        must_query.append(Q("terms", project_version_id=[project_version_id]))
    if search_keyword:
        must_query.append(
            Q("wildcard", **{"package_name.keyword": {"value": f"*{search_keyword}*"}})
        )
    Q("bool", must=must_query)
    search = IastAssetDocument.search().query(Q("bool", must=must_query))[:0]
    buckets = {
        "level": A("terms", field="level_id", size=2147483647),
        "language": A("terms", field="language.keyword", size=2147483647),
        **extend_aggs_buckets,
    }
    for k, v in buckets.items():
        search.aggs.bucket(k, v).bucket(
            "distinct_signature_value",
            A("cardinality", field="signature_value.keyword"),
        )
    res = search.using(
        Elasticsearch(settings.ELASTICSEARCH_DSL["default"]["hosts"])
    ).execute()
    dic = {}
    for key in buckets:
        origin_buckets = res.aggs[key].to_dict()["buckets"]
        for i in origin_buckets:
            i["id"] = i["key"]
            del i["key"]
            i["count"] = i["distinct_signature_value"]["value"]
            del i["distinct_signature_value"]
            del i["doc_count"]
        if key == "language":
            for i in origin_buckets:
                i["language"] = i["id"]
                del i["id"]
            language_names = [i["language"] for i in origin_buckets]
            for i in origin_buckets:
                i["id"] = LANGUAGE_DICT.get(i["language"])
            for language_key in LANGUAGE_DICT:
                if language_key not in language_names:
                    origin_buckets.append(
                        {
                            "id": LANGUAGE_DICT[language_key],
                            "language": language_key,
                            "count": 0,
                        }
                    )
        if key == "level":
            for i in origin_buckets:
                i["level_id"] = i["id"]
                del i["id"]
            level_ids = [i["level_id"] for i in origin_buckets]
            level = IastVulLevel.objects.values("id", "name_value").all()
            level_dic = dict_transfrom(level, "id")
            for i in origin_buckets:
                i["level"] = level_dic[i["level_id"]]["name_value"]
            for level_id in level_dic:
                if level_id not in level_ids:
                    origin_buckets.append(
                        {
                            "level_id": level_id,
                            "level": level_dic[level_id]["name_value"],
                            "count": 0,
                        }
                    )

        dic[key] = list(origin_buckets)
    return dic, res
