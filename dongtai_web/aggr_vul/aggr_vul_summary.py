from dongtai_conf.settings import ELASTICSEARCH_STATE
import copy

from dongtai_common.endpoint import UserEndPoint
from dongtai_web.utils import extend_schema_with_envcheck
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import R
from dongtai_common.models import LANGUAGE_DICT
from rest_framework.serializers import ValidationError
from django.db import connection
from dongtai_common.common.utils import cached_decorator
from dongtai_common.models import APP_LEVEL_RISK
from dongtai_common.models.user import User
from typing import TypedDict


class Level(TypedDict):
    name: str
    num: int
    id: int


class AvailabilityDetail(TypedDict):
    name: str
    num: int
    id: int


class Availability(TypedDict):
    have_poc: AvailabilityDetail
    have_article: AvailabilityDetail
    no_availability: AvailabilityDetail


class BaseSummary(TypedDict):
    level: list[Level]
    availability: Availability
    hook_type: list
    language: list
    project: list


def get_annotate_sca_common_data(user_id: int, pro_condition: str):
    return get_annotate_sca_base_data(user_id, pro_condition)


@cached_decorator(random_range=(2 * 60 * 60, 2 * 60 * 60), use_celery_update=True)
def get_annotate_sca_cache_data(user_id: int):
    return get_annotate_sca_base_data(user_id, "")


def get_annotate_sca_base_data(user_id: int, pro_condition: str):
    base_summary: BaseSummary = {
        "level": [],
        "availability": {
            "have_poc": {"name": "存在利用代码", "num": 0, "id": 1},
            "have_article": {"name": "存在分析文章", "num": 0, "id": 2},
            "no_availability": {"name": "无利用信息", "num": 0, "id": 3},
        },
        "hook_type": [],
        "language": [],
        "project": [],
    }
    user = User.objects.get(pk=user_id)
    departments = list(user.get_relative_department())
    department_filter_sql = " and {}.department_id in ({})".format(
        "asset", ",".join(str(x.id) for x in departments)
    )
    query_condition = (
        " where rel.is_del=0 and asset.project_id>0 "
        + department_filter_sql
        + pro_condition
    )
    base_join = (
        "left JOIN iast_asset_vul_relation as rel on rel.asset_vul_id=vul.id  "
        "left JOIN iast_asset as asset on rel.asset_id=asset.id "
    )

    with connection.cursor() as cursor:
        count_level_query = (
            "SELECT  vul.level_id,count( DISTINCT(vul.id ))  from iast_asset_vul as vul  "
            + base_join
            + query_condition
            + " group by vul.level_id  "
        )
        result_summary = base_summary

        cursor.execute(count_level_query)
        level_summary = cursor.fetchall()
        if level_summary:
            for item in level_summary:
                level_id, count = item
                result_summary["level"].append(
                    {
                        "name": APP_LEVEL_RISK.get(str(level_id), "None"),
                        "num": count,
                        "id": level_id,
                    }
                )

        # 存在利用代码
        count_poc_query = (
            "SELECT COUNT(*) as have_poc_count FROM (SELECT DISTINCT( vul.id )  from iast_asset_vul as vul  "
            + base_join
            + query_condition
            + " and  vul.have_poc=1 ) temp"
        )
        cursor.execute(count_poc_query)
        poc_summary = cursor.fetchone()
        if poc_summary:
            result_summary["availability"]["have_poc"]["num"] = poc_summary[0]
        # 存在分析文章
        count_article_query = (
            "SELECT COUNT(*) as have_article_count FROM ( SELECT DISTINCT( vul.id ) from iast_asset_vul as vul  "
            + base_join
            + query_condition
            + " and  vul.have_article=1 ) temp"
        )
        cursor.execute(count_article_query)
        article_summary = cursor.fetchone()
        if article_summary:
            result_summary["availability"]["have_article"]["num"] = article_summary[0]
        # 无利用信息
        count_no_availability_query = (
            "SELECT COUNT(*) FROM (SELECT DISTINCT( vul.id ) as no_availability from iast_asset_vul as vul  "
            + base_join
            + query_condition
            + " and  vul.have_article=0 and  vul.have_poc=0) temp "
        )
        cursor.execute(count_no_availability_query)
        no_availability_summary = cursor.fetchone()
        if no_availability_summary:
            result_summary["availability"]["no_availability"][
                "num"
            ] = no_availability_summary[0]

        count_language_query = (
            "SELECT  vul.package_language, count( DISTINCT(vul.id )) AS count_package_language  from iast_asset_vul as vul  "
            + base_join
            + query_condition
            + " group by vul.package_language  "
        )
        cursor.execute(count_language_query)
        language_summary = cursor.fetchall()
        lang_arr = copy.copy(LANGUAGE_DICT)
        lang_key = lang_arr.keys()
        if language_summary:
            for item in language_summary:
                package_language, count_package_language = item
                result_summary["language"].append(
                    {
                        "id": lang_arr.get(str(package_language)),
                        "num": count_package_language,
                        "name": package_language,
                    }
                )
                if package_language in lang_key:
                    del lang_arr[package_language]
        if lang_arr:
            for item in lang_arr:
                result_summary["language"].append(
                    {"id": LANGUAGE_DICT.get(item), "num": 0, "name": item}
                )

        # 漏洞类型 统计
        vul_type_join = (
            "left JOIN iast_asset_vul_type_relation as typeR on vul.id=typeR.asset_vul_id "
            "left JOIN iast_asset_vul_type as typeInfo on typeInfo.id=typeR.asset_vul_type_id "
        )
        count_vul_type_query = (
            "SELECT  typeR.asset_vul_type_id as vul_type_id, count( DISTINCT(vul.id )) AS count_vul_type, "
            "typeInfo.name as type_name   from iast_asset_vul as vul  "
            + base_join
            + vul_type_join
            + query_condition
            + " group by typeR.asset_vul_type_id  "
        )
        cursor.execute(count_vul_type_query)
        type_summary = cursor.fetchall()
        if type_summary:
            for item in type_summary:
                vul_type_id, count_vul_type, type_name = item
                result_summary["hook_type"].append(
                    {"id": vul_type_id, "num": count_vul_type, "name": type_name}
                )
        # 归属项目 统计
        count_project_query = (
            " SELECT project_id, _count, name AS project_name FROM iast_project AS ip RIGHT  JOIN ( SELECT asset.project_id AS project_id, count( DISTINCT(vul.id ))  AS _count "
            "  from iast_asset_vul as vul  "
            + base_join
            + query_condition
            + " and asset.project_id>0 group by asset.project_id )   temp ON ip.id = temp.project_id "
        )
        cursor.execute(count_project_query)
        project_summary = cursor.fetchall()
        if project_summary:
            for item in project_summary:
                project_id, count_project, project_name = item
                result_summary["project"].append(
                    {"id": project_id, "num": count_project, "name": project_name}
                )

    return result_summary


def get_annotate_data_es(user_id, bind_project_id=None, project_version_id=None):
    from dongtai_common.models.vulnerablity import IastVulnerabilityDocument
    from elasticsearch_dsl import Q, Search
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import A
    from dongtai_common.models.strategy import IastStrategyModel
    from dongtai_common.models.vulnerablity import IastVulnerabilityStatus
    from dongtai_common.models.program_language import IastProgramLanguage
    from dongtai_common.models.project import IastProject
    from dongtai_common.models.vul_level import IastVulLevel
    from dongtai_common.models.asset_vul import IastAssetVulnerabilityDocument
    from dongtai_conf import settings
    from dongtai_web.utils import dict_transfrom

    user = User.objects.get(pk=user_id)
    departments = list(user.get_relative_department())
    department_ids = [i.id for i in departments]
    must_query = [
        Q("terms", asset_department_id=department_ids),
        Q("terms", asset_vul_relation_is_del=[0]),
        Q("range", asset_project_id={"gt": 0}),
    ]
    if bind_project_id:
        must_query.append(Q("terms", asset_project_id=[bind_project_id]))
    if project_version_id:
        must_query.append(Q("terms", asset_project_version_id=[project_version_id]))
    search = IastAssetVulnerabilityDocument.search().query(Q("bool", must=must_query))[
        :0
    ]
    buckets = {
        "level": A("terms", field="level_id", size=2147483647),
        "project": A("terms", field="asset_project_id", size=2147483647),
        "language": A("terms", field="package_language.keyword", size=2147483647),
    }
    for k, v in buckets.items():
        search.aggs.bucket(k, v).bucket(
            "distinct_asset_vul", A("cardinality", field="asset_vul_id")
        )
    search.aggs.bucket("poc", A("terms", field="have_poc", size=2147483647)).bucket(
        "article", A("terms", field="have_article", size=2147483647)
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
            i["num"] = i["distinct_asset_vul"]["value"]
            del i["distinct_asset_vul"]
            del i["doc_count"]
        if key == "language":
            for i in origin_buckets:
                i["name"] = i["id"]
                del i["id"]
            language_names = [i["name"] for i in origin_buckets]
            for i in origin_buckets:
                i["id"] = LANGUAGE_DICT.get(i["name"])
            for language_key in LANGUAGE_DICT:
                if language_key not in language_names:
                    origin_buckets.append(
                        {
                            "id": LANGUAGE_DICT[language_key],
                            "name": language_key,
                            "num": 0,
                        }
                    )
        if key == "project":
            project_ids = [i["id"] for i in origin_buckets]
            project = (
                IastProject.objects.filter(pk__in=project_ids)
                .values("id", "name")
                .all()
            )
            project_dic = dict_transfrom(project, "id")
            for i in origin_buckets:
                if project_dic.get(i["id"], None):
                    i["name"] = project_dic[i["id"]]["name"]
                else:
                    del i
        if key == "level":
            level_ids = [i["id"] for i in origin_buckets]
            level = (
                IastVulLevel.objects.filter(pk__in=level_ids)
                .values("id", "name_value")
                .all()
            )
            level_dic = dict_transfrom(level, "id")
            for i in origin_buckets:
                i["name"] = level_dic[i["id"]]["name_value"]
        dic[key] = list(origin_buckets)
    have_article_count = 0
    have_poc_count = 0
    no_usable_count = 0
    for i in res.aggs["poc"].to_dict()["buckets"]:
        if i["key"] == 1:
            have_poc_count = i["doc_count"]
            for k in i["article"]["buckets"]:
                if k["key"] == 1:
                    have_article_count += int(k["doc_count"])
        if i["key"] == 0:
            for k in i["article"]["buckets"]:
                if k["key"] == 1:
                    have_article_count += int(k["doc_count"])
                if k["key"] == 0:
                    no_usable_count = k["doc_count"]

    dic["availability"] = {
        "have_poc": {"name": "存在利用代码", "num": have_poc_count, "id": 1},
        "have_article": {"name": "存在分析文章", "num": have_article_count, "id": 2},
        "no_availability": {"name": "无利用信息", "num": no_usable_count, "id": 3},
    }
    return dic


class GetScaSummary(UserEndPoint):
    name = "api-v1-aggregation-summary"
    description = _("New application")

    @extend_schema_with_envcheck(
        request=AggregationArgsSerializer,
        tags=[_("漏洞")],
        summary=_("组件漏洞列表"),
        description=_("count sca vul and app vul by keywords"),
    )
    def post(self, request):
        ser = AggregationArgsSerializer(data=request.data)
        pro_condition = ""
        try:
            if ser.is_valid(True):
                # 从项目列表进入 绑定项目id
                if ser.validated_data.get("bind_project_id", 0):
                    pro_condition = pro_condition + " and asset.project_id={} ".format(
                        str(ser.validated_data.get("bind_project_id"))
                    )
                # 项目版本号
                if ser.validated_data.get("project_version_id", 0):
                    pro_condition = (
                        pro_condition
                        + " and asset.project_version_id={} ".format(
                            str(ser.validated_data.get("project_version_id"))
                        )
                    )
        except ValidationError as e:
            return R.failure(data=e.detail)

        if ELASTICSEARCH_STATE:
            result_summary = get_annotate_data_es(
                request.user.id,
                ser.validated_data.get("bind_project_id", 0),
                ser.validated_data.get("project_version_id", 0),
            )
        elif pro_condition:
            # 存在项目筛选条件
            result_summary = get_annotate_sca_common_data(
                request.user.id, pro_condition
            )
        else:
            # 全局数据,没有项目信息 数据按用户id缓存
            result_summary = get_annotate_sca_cache_data(request.user.id)

        return R.success(
            data={"messages": result_summary},
        )
