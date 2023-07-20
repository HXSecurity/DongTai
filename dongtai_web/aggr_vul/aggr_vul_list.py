# 按类型获取 组件漏洞 应用漏洞列表
from typing import Any
from elasticsearch_dsl import Q
from dongtai_common.models.asset_vul import IastAssetVulnerabilityDocument
from dongtai_common.common.utils import make_hash
from dongtai_conf import settings
from django.core.cache import cache
from elasticsearch import Elasticsearch
import logging
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint

from dongtai_web.utils import extend_schema_with_envcheck
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _
from dongtai_web.aggregation.aggregation_common import (
    turnIntListOfStr,
    auth_user_list_str,
)
import pymysql
from dongtai_web.serializers.vul import VulSerializer
from dongtai_common.models.asset_vul import (
    IastAssetVul,
    IastVulAssetRelation,
    IastAssetVulTypeRelation,
)
from dongtai_common.models import (
    AGGREGATION_ORDER,
    LANGUAGE_ID_DICT,
    APP_LEVEL_RISK,
    LICENSE_RISK,
    SCA_AVAILABILITY_DICT,
)
from dongtai_conf.settings import ELASTICSEARCH_STATE
from dongtai_common.models.asset import Asset
from django.db.models import Max
from dongtai_common.models.user import User

logger = logging.getLogger("django")
INT_LIMIT: int = 2**64 - 1


def convert_cwe(cwe: list | str) -> str:
    if isinstance(cwe, list):
        if len(cwe) > 0:
            return cwe[0].replace("CWE-", "")
        return ""
    if isinstance(cwe, str):
        return cwe.replace("CWE-", "")
    return ""


def get_cve_from_cve_nums(cve_nums: dict) -> str:
    cwe = cve_nums.get("cwe", [])
    return convert_cwe(cwe)


class GetAggregationVulList(UserEndPoint):
    name = "api-v1-aggregation-vul-list"
    description = _("New application")

    @extend_schema_with_envcheck(
        request=AggregationArgsSerializer,
        tags=[_("漏洞")],
        summary=_("组件漏洞列表"),
        description=_("select sca vul and app vul by keywords"),
    )
    # 组件漏洞 列表
    def post(self, request):
        ser = AggregationArgsSerializer(data=request.data)
        keywords = ""
        join_table = ""
        query_condition = " where rel.is_del=0 "
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data["page_size"]
                page = ser.validated_data["page"]
                begin_num = (page - 1) * page_size
                end_num = page * page_size
                # should refact into serilizer
                if begin_num > INT_LIMIT or end_num > INT_LIMIT:
                    return R.failure()
                keywords = ser.validated_data.get("keywords", "")
                es_query = {}
                if keywords:
                    keywords = pymysql.converters.escape_string(keywords)
                    keywords = "+" + keywords
                    es_query["search_keyword"] = ser.validated_data.get("keywords", "")
                order_type = AGGREGATION_ORDER.get(
                    str(ser.validated_data["order_type"]), "vul.level_id"
                )
                order_type_desc = (
                    "desc" if ser.validated_data["order_type_desc"] else "asc"
                )
                es_dict = {"1": "level_id", "2": "create_time", "3": "vul_update_time"}
                order_type_es = es_dict.get(
                    str(ser.validated_data["order_type"]), "level_id"
                )
                es_query["order"] = {order_type_es: {"order": order_type_desc}}
                # 从项目列表进入 绑定项目id
                if ser.validated_data.get("bind_project_id", 0):
                    query_condition = (
                        query_condition
                        + " and asset.project_id={} ".format(
                            str(ser.validated_data.get("bind_project_id"))
                        )
                    )
                    es_query["bind_project_id"] = ser.validated_data.get(
                        "bind_project_id"
                    )
                # 项目版本号
                if ser.validated_data.get("project_version_id", 0):
                    query_condition = (
                        query_condition
                        + " and asset.project_version_id={} ".format(
                            str(ser.validated_data.get("project_version_id"))
                        )
                    )
                    es_query["project_version_id"] = ser.validated_data.get(
                        "project_version_id"
                    )
                # 按项目筛选
                if ser.validated_data.get("project_id_str", ""):
                    project_str = turnIntListOfStr(
                        ser.validated_data.get("project_id_str", ""), "asset.project_id"
                    )
                    query_condition = query_condition + project_str
                    es_query["project_ids"] = turnIntListOfStr(
                        ser.validated_data.get("project_id_str")
                    )
                # 按语言筛选
                if ser.validated_data.get("language_str", ""):
                    language_str = ser.validated_data.get("language_str", "")
                    type_list = language_str.split(",")
                    # 安全校验,强制转int
                    type_list = list(map(int, type_list))
                    type_int_list = list(map(str, type_list))
                    lang_str = []
                    for one_type in type_int_list:
                        lang_str.append("'" + LANGUAGE_ID_DICT.get(one_type, "") + "'")
                    type_int_str = ",".join(lang_str)
                    language_str_change = " and {} in ({}) ".format(
                        "vul.package_language", type_int_str
                    )
                    query_condition = query_condition + language_str_change
                    language_id_list = turnIntListOfStr(
                        ser.validated_data.get("language_str", "")
                    )
                    language_arr = []
                    for lang in language_id_list:
                        language_arr.append(LANGUAGE_ID_DICT.get(str(lang)))
                    es_query["language_ids"] = language_arr
                # 漏洞类型筛选 弃用
                if ser.validated_data.get("hook_type_id_str", ""):
                    vul_type_str = turnIntListOfStr(
                        ser.validated_data.get("hook_type_id_str", ""),
                        "typeR.asset_vul_type_id",
                    )
                    query_condition = query_condition + vul_type_str
                    join_table = (
                        join_table
                        + "left JOIN iast_asset_vul_type_relation as typeR on vul.id=typeR.asset_vul_id "
                    )
                # 漏洞等级筛选
                if ser.validated_data.get("level_id_str", ""):
                    status_str = turnIntListOfStr(
                        ser.validated_data.get("level_id_str", ""), "vul.level_id"
                    )
                    query_condition = query_condition + status_str
                    es_query["level_ids"] = turnIntListOfStr(
                        ser.validated_data.get("level_id_str")
                    )
                # 可利用性
                if ser.validated_data.get("availability_str", ""):
                    availability_arr = turnIntListOfStr(
                        ser.validated_data.get("availability_str", "")
                    )
                    # there is a bug, and it has been fix in validator.
                    # in fact, a more reasonable approch is use serializer to
                    # handle the cover in prepose.
                    if 3 in availability_arr:
                        query_condition = (
                            query_condition
                            + " and vul.have_article=0 and vul.have_poc=0 "
                        )
                    else:
                        if 1 in availability_arr:
                            query_condition = query_condition + " and vul.have_poc=1 "
                        if 2 in availability_arr:
                            query_condition = (
                                query_condition + " and vul.have_article=1 "
                            )
                    es_query["availability_ids"] = turnIntListOfStr(
                        ser.validated_data.get("availability_str")
                    )

        except ValidationError as e:
            return R.failure(data=e.detail)
        departments = list(request.user.get_relative_department())
        department_filter_sql = " and {}.department_id in ({})".format(
            "asset", ",".join(str(x.id) for x in departments)
        )
        query_condition = query_condition + department_filter_sql

        if keywords:
            query_base = (
                "SELECT DISTINCT(vul.id),vul.id,vul.level_id,vul.update_time_desc,vul.update_time,"
                " MATCH( `vul`.`vul_name`,`vul`.`aql`,`vul`.`vul_serial` ) AGAINST ( %s IN NATURAL LANGUAGE MODE ) AS `score`"
                "  from iast_asset_vul as vul  "
                "left JOIN  iast_asset_vul_relation as rel  on rel.asset_vul_id=vul.id  "
                "left JOIN iast_asset as asset on rel.asset_id=asset.id  "
                + join_table
                + query_condition
            )

        else:
            query_base = (
                "SELECT DISTINCT(vul.id),vul.id,vul.level_id,vul.update_time_desc,vul.update_time from iast_asset_vul as vul "
                "left JOIN iast_asset_vul_relation as rel on rel.asset_vul_id=vul.id  "
                "left JOIN iast_asset as asset on rel.asset_id=asset.id  "
                + join_table
                + query_condition
            )

        # mysql 全文索引下,count不准确,等于全部数量
        new_order = order_type + " " + order_type_desc
        if order_type == "vul.level_id":
            if order_type_desc == "desc":
                new_order = new_order + ", vul.update_time desc"
            else:
                new_order = new_order + ", vul.update_time_desc"

        if ELASTICSEARCH_STATE:
            all_vul = get_vul_list_from_elastic_search(
                request.user.id,
                page_size=ser.validated_data["page_size"],
                page=ser.validated_data["page"],
                **es_query,
            )
        else:
            if keywords:
                all_vul = IastAssetVul.objects.raw(
                    query_base
                    + "  order by score desc, {} limit {},{};  ".format(
                        new_order, begin_num, end_num
                    ),
                    [keywords],
                )
            else:
                all_vul = IastAssetVul.objects.raw(
                    query_base
                    + f"  order by {new_order}  limit {begin_num},{end_num};  "
                )
            all_vul = IastAssetVul.objects.filter(
                pk__in=[vul.id for vul in all_vul]
            ).all()
        content_list = []

        if all_vul:
            vul_ids = []
            for item in all_vul:
                # 拼写 漏洞类型
                # 拼写 漏洞编号
                availability_arr = []
                if item.have_poc:
                    availability_arr.append(SCA_AVAILABILITY_DICT.get("1"))
                if item.have_article:
                    availability_arr.append(SCA_AVAILABILITY_DICT.get("2"))
                if not availability_arr:
                    availability_arr.append(SCA_AVAILABILITY_DICT.get("3"))
                availability_str = ",".join(availability_arr)
                cur_data = {
                    "id": item.id,
                    "vul_name": item.vul_name,
                    "create_time": item.create_time,
                    "level_id": item.level_id,
                    "level_name": APP_LEVEL_RISK.get(str(item.level_id), ""),
                    "license": item.license,
                    "license_level": item.license_level,
                    "license_risk_name": LICENSE_RISK.get(str(item.license_level), ""),
                    "vul_cve_nums": item.vul_cve_nums,
                    "package_name": item.package_name,
                    "package_safe_version": item.package_safe_version,
                    "package_latest_version": item.package_latest_version,
                    "package_language": item.package_language,
                    "availability_str": availability_str,
                }
                if cur_data["vul_cve_nums"]:
                    cwe = get_cve_from_cve_nums(cur_data["vul_cve_nums"])
                    if cwe:
                        cur_data["vul_cve_nums"]["cwe_num"] = cwe
                vul_ids.append(item.id)
                content_list.append(cur_data)
            # 追加 用户 权限
            afdistset = (
                Asset.objects.filter(
                    iastvulassetrelation__asset_vul_id__in=vul_ids,
                    iastvulassetrelation__is_del=0,
                    department__in=departments,
                    project_id__gt=0,
                )
                .values("project_id", "iastvulassetrelation__asset_vul_id")
                .annotate(aid=Max("id"))
                .all()
            )

            pro_info = (
                IastVulAssetRelation.objects.filter(
                    asset_vul_id__in=[
                        i["iastvulassetrelation__asset_vul_id"] for i in afdistset
                    ],
                    asset_id__in=[i["aid"] for i in afdistset],
                )
                .values(
                    "asset_vul_id",
                    "asset__project_id",
                    "asset__project_name",
                    "asset__project_version__version_name",
                    "asset__project_version_id",
                    "asset__agent__server__container",
                )
                .distinct()
            )
            pro_arr = {}
            for item in pro_info:
                vul_id = item["asset_vul_id"]
                item["server_type"] = VulSerializer.split_container_name(
                    item["asset__agent__server__container"]
                )
                del item["asset_vul_id"]
                if pro_arr.get(vul_id, []):
                    pro_arr[vul_id].append(item)
                else:
                    pro_arr[vul_id] = [item]
            # 根据vul_id获取对应的漏洞类型 一对多
            type_info = IastAssetVulTypeRelation.objects.filter(
                asset_vul_id__in=vul_ids
            ).values("asset_vul_id", "asset_vul_type__name")
            type_arr = {}
            for item in type_info:
                if not type_arr.get(item["asset_vul_id"], []):
                    type_arr[item["asset_vul_id"]] = [item["asset_vul_type__name"]]
                elif item["asset_vul_type__name"] not in type_arr[item["asset_vul_id"]]:
                    type_arr[item["asset_vul_id"]].append(item["asset_vul_type__name"])
            for row in content_list:
                row["pro_info"] = pro_arr.get(row["id"], [])
                row["type_name"] = ",".join(type_arr.get(row["id"], []))
            set_vul_inetration(content_list, vul_ids, request.user.id)
        return R.success(
            data={
                "messages": content_list,
                "page": {"page_size": page_size, "cur_page": page},
            },
        )


def set_vul_inetration(
    content_list: list[dict[str, Any]],
    vul_ids: list[int],
    user_id: int,
) -> None:
    pass


def get_vul_list_from_elastic_search(
    user_id,
    project_ids=[],
    project_version_ids=[],
    level_ids=[],
    language_ids=[],
    availability_ids=[],
    search_keyword="",
    page=1,
    page_size=10,
    bind_project_id=0,
    project_version_id=0,
    order={},
):
    auth_user_info = auth_user_list_str(user_id=user_id)
    auth_user_info["user_list"]
    user = User.objects.filter(pk=user_id).first()
    departments = user.get_relative_department()
    department_ids = [department.id for department in departments]
    must_query = [
        Q("terms", asset_department_id=department_ids),
        Q("terms", asset_vul_relation_is_del=[0]),
        Q("range", asset_project_id={"gt": 0}),
    ]
    order_list = ["update_time", "-asset_vul_relation_id", "asset_vul_id"]
    if order:
        order_list.insert(0, order)
    if bind_project_id:
        must_query.append(Q("terms", asset_project_id=[bind_project_id]))
    if project_version_id:
        must_query.append(Q("terms", asset_project_version_id=[project_version_id]))
    if project_ids:
        must_query.append(Q("terms", asset_project_id=project_ids))
    if project_version_ids:
        must_query.append(Q("terms", asset_project_version_id=project_version_ids))
    if level_ids:
        must_query.append(Q("terms", level_id=level_ids))
    if language_ids:
        must_query.append(Q("terms", **{"package_language.keyword": language_ids}))
    if availability_ids:
        sub_bool_query = []
        for availability in availability_ids:
            if availability == 3:
                sub_bool_query.append(Q("terms", have_article=[0]))
                sub_bool_query.append(Q("terms", have_poc=[0]))
            elif availability == 1:
                sub_bool_query.append(Q("terms", have_poc=[1]))
            elif availability == 2:
                sub_bool_query.append(Q("terms", have_article=[1]))
        must_query.append(Q("bool", should=sub_bool_query))

    if search_keyword:
        must_query.append(
            Q(
                "multi_match",
                query=search_keyword,
                fields=["vul_name", "vul_serial", "aql"],
            )
        )
    hashkey = make_hash(
        [
            user_id,
            project_ids,
            project_version_ids,
            level_ids,
            language_ids,
            search_keyword,
            page_size,
            bind_project_id,
            project_version_id,
        ]
    )
    after_table = cache.get(hashkey, {})
    after_key = after_table.get(page, None)
    extra_dict = {}
    if after_key:
        sub_after_must_query = []
        sub_after_should_query = []
        for info, value in zip(order_list, after_key):
            field = ""
            opt = ""
            if isinstance(info, dict):
                field = list(info.keys())[0]
                opt = "lt" if info[field]["order"] == "desc" else "gt"
            if isinstance(info, str):
                if info.startswith("-"):
                    field = info[1::]
                    opt = "lt"
                else:
                    field = info
                    opt = "gt"
            if info == "asset_vul_id":
                sub_after_must_query.append(Q("range", **{field: {opt: value}}))
            else:
                sub_after_should_query.append(Q("range", **{field: {opt: value}}))
        must_query.append(
            Q(
                "bool",
                must=sub_after_must_query,
                should=sub_after_should_query,
                minimum_should_match=1,
            )
        )
    a = Q("bool", must=must_query)
    res = (
        IastAssetVulnerabilityDocument.search()
        .query(a)
        .extra(collapse={"field": "asset_vul_id"})
        .extra(**extra_dict)
        .sort(*order_list)[:page_size]
        .using(Elasticsearch(settings.ELASTICSEARCH_DSL["default"]["hosts"]))
    )
    resp = res.execute()
    vuls = [i._d_ for i in list(resp)]
    if resp.hits:
        afterkey = resp.hits[-1].meta["sort"]
        after_table[page + 1] = afterkey
        cache.set(hashkey, after_table)
    keymaps = {"asset_vul_id": "id"}
    for i in vuls:
        for k, v in keymaps.items():
            i[v] = i[k]
            del i[k]
    from collections import namedtuple
    import json

    namedtuple_vuls = []
    if vuls:
        keys = [
            "vul_cve_nums",
            "asset_project_version_id",
            "license_level",
            "cve_code",
            "asset_id",
            "asset_project_id",
            "vul_publish_time",
            "update_time_desc",
            "package_language",
            "have_poc",
            "search_title",
            "package_safe_version",
            "asset_user_id",
            "package_version",
            "vul_update_time",
            "update_time",
            "asset_vul_relation_id",
            "vul_name",
            "have_article",
            "level_id",
            "vul_detail",
            "asset_agent_id",
            "package_name",
            "vul_serial",
            "create_time",
            "package_hash",
            "license",
            "cve_id",
            "aql",
            "package_latest_version",
            "asset_vul_relation_is_del",
            "id",
        ]
        AssetVul = namedtuple("AssetVul", keys)
        for i in vuls:
            i["vul_cve_nums"] = json.loads(i["vul_cve_nums"])
            if "@timestamp" in i:
                del i["@timestamp"]
            for key in keys:
                if key not in i.keys():
                    i[key] = None
            i["id"] = i["id"][0]
            dic = {}
            for k, v in i.items():
                if k in keys:
                    dic[k] = v
            asset_vul = AssetVul(**dic)
            namedtuple_vuls.append(asset_vul)
    return namedtuple_vuls
