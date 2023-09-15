from collections import defaultdict
from itertools import groupby
from typing import Any

import pymysql
from django.core.cache import cache
from django.db.models import Count, F
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.common.utils import make_hash
from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models import APP_LEVEL_RISK, APP_VUL_ORDER
from dongtai_common.models.agent_method_pool import VulMethodPool
from dongtai_common.models.dast_integration import IastDastIntegrationRelation
from dongtai_common.models.vulnerablity import (
    IastVulnerabilityDocument,
    IastVulnerabilityModel,
    IastVulnerabilityStatus,
)
from dongtai_common.utils.const import OPERATE_GET
from dongtai_common.utils.db import SearchLanguageMode
from dongtai_conf import settings
from dongtai_conf.patch import patch_point, to_patch
from dongtai_conf.settings import ELASTICSEARCH_STATE
from dongtai_engine.elatic_search.data_correction import data_correction_interpetor
from dongtai_web.aggregation.aggregation_common import turnIntListOfStr
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from dongtai_web.serializers.vul import VulSerializer
from dongtai_web.utils import get_response_serializer

INT_LIMIT: int = 2**64 - 1


class AppVulSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField()
    server_type = serializers.CharField()
    is_header_vul = serializers.CharField()
    agent__project_name = serializers.CharField()
    agent__server__container = serializers.CharField()
    agent__language = serializers.CharField()
    agent__bind_project_id = serializers.CharField()
    header_vul_urls = serializers.ListField()
    dastvul__vul_type = serializers.CharField()
    dastvul_count = serializers.CharField()
    dast_validation_status = serializers.CharField()
    strategy__vul_name = serializers.CharField()
    project__name = serializers.CharField()
    server__container = serializers.CharField()
    project_version__version_name = serializers.CharField()

    class Meta:
        model = IastVulnerabilityModel
        fields = [
            "id",
            "uri",
            "http_method",
            "top_stack",
            "bottom_stack",
            "level_id",
            "taint_position",
            "status_id",
            "first_time",
            "latest_time",
            "strategy__vul_name",
            "language",
            "project__name",
            "server__container",
            "project_id",
            "strategy_id",
            "project_version_id",
            "project_version__version_name",
            "level_name",
            "server_type",
            "is_header_vul",
            "agent__project_name",
            "agent__server__container",
            "agent__language",
            "agent__bind_project_id",
            "header_vul_urls",
            "dastvul__vul_type",
            "dastvul_count",
            "dast_validation_status",
        ]


_NewResponseSerializer = get_response_serializer(AppVulSerializer(many=True))


class GetAppVulsList(UserEndPoint):
    @extend_schema(
        request=AggregationArgsSerializer,
        tags=[_("Vulnerability"), OPERATE_GET, "集成"],
        summary="应用漏洞列表",
    )
    @to_patch
    def post(self, request):
        """
        :param request:
        :return:
        """
        end = {
            "status": 201,
            "msg": "success",
            "data": [],
        }
        ser = AggregationArgsSerializer(data=request.data)
        # 获取用户权限
        projects = request.user.get_projects()
        queryset = IastVulnerabilityModel.objects.filter(is_del=0, project_id__gt=0, project__in=projects)

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
                # 从项目列表进入 绑定项目id
                if ser.validated_data.get("bind_project_id", 0):
                    queryset = queryset.filter(project_id=ser.validated_data.get("bind_project_id"))
                    es_query["bind_project_id"] = ser.validated_data.get("bind_project_id")
                # 项目版本号
                if ser.validated_data.get("project_version_id", 0):
                    queryset = queryset.filter(project_version_id=ser.validated_data.get("project_version_id"))
                    es_query["project_version_id"] = ser.validated_data.get("project_version_id")
                ser, queryset, es_query = patch_point(ser, queryset, es_query)
                if ser.validated_data.get("uri", ""):
                    queryset = queryset.filter(uri=ser.validated_data.get("uri", ""))
                # 漏洞类型筛选
                if ser.validated_data.get("hook_type_id_str", ""):
                    vul_type_list = turnIntListOfStr(ser.validated_data.get("hook_type_id_str", ""))
                    queryset = queryset.filter(strategy_id__in=vul_type_list)
                    es_query["strategy_ids"] = vul_type_list
                # 漏洞等级筛选
                if ser.validated_data.get("level_id_str", ""):
                    level_id_list = turnIntListOfStr(ser.validated_data.get("level_id_str", ""))
                    queryset = queryset.filter(level_id__in=level_id_list)
                    es_query["level_ids"] = level_id_list
                # 按状态筛选
                if ser.validated_data.get("status_id_str", ""):
                    status_id_list = turnIntListOfStr(ser.validated_data.get("status_id_str", ""))
                    queryset = queryset.filter(status_id__in=status_id_list)
                    es_query["status_ids"] = status_id_list

                order_list = []
                fields = [
                    "id",
                    "uri",
                    "http_method",
                    "top_stack",
                    "bottom_stack",
                    "level_id",
                    "taint_position",
                    "status_id",
                    "first_time",
                    "latest_time",
                    "strategy__vul_name",
                    "language",
                    "project__name",
                    "server__container",
                    "project_id",
                    "strategy_id",
                    "project_version_id",
                    "project_version__version_name",
                ]
                if keywords:
                    es_query["search_keyword"] = keywords
                    keywords = pymysql.converters.escape_string(keywords)
                    order_list = ["-score"]
                    fields.append("score")

                    queryset = queryset.annotate(
                        score=SearchLanguageMode(
                            [
                                F("search_keywords"),
                                F("uri"),
                                F("vul_title"),
                                F("http_method"),
                                F("http_protocol"),
                                F("top_stack"),
                                F("bottom_stack"),
                            ],
                            search_keyword="+" + keywords,
                        )
                    )
                # 排序
                order_type = APP_VUL_ORDER.get(str(ser.validated_data["order_type"]), "level_id")
                order_type_desc = "-" if ser.validated_data["order_type_desc"] else ""
                if order_type == "level_id":
                    order_list.append(order_type_desc + order_type)
                    if ser.validated_data["order_type_desc"]:
                        order_list.append("-latest_time")
                    else:
                        order_list.append("latest_time_desc")
                else:
                    order_list.append(order_type_desc + order_type)
                es_query["order"] = order_type_desc + order_type
                if ELASTICSEARCH_STATE:
                    vul_data = get_vul_list_from_elastic_search(projects, page=page, page_size=page_size, **es_query)
                else:
                    vul_data = queryset.values(*tuple(fields)).order_by(*tuple(order_list))[begin_num:end_num]
        except ValidationError as e:
            return R.failure(data=e.detail)
        vul_ids = [vul["id"] for vul in vul_data]
        dastvul_rel_count_res = (
            IastDastIntegrationRelation.objects.filter(iastvul_id__in=vul_ids)
            .values("iastvul_id")
            .annotate(dastvul_count=Count("dastvul_id"))
        )
        dast_vul_types = (
            IastDastIntegrationRelation.objects.filter(
                iastvul_id__in=vul_ids,
                dastvul__vul_type__isnull=False,
            )
            .values("dastvul__vul_type", "iastvul_id")
            .distinct()
        )
        dast_vul_types_dict = defaultdict(
            list,
            {
                k: list({x["dastvul__vul_type"] for x in g})
                for k, g in groupby(dast_vul_types, key=lambda x: x["iastvul_id"])
            },
        )
        dastvul_rel_count_res_dict = defaultdict(
            lambda: 0,
            {item["iastvul_id"]: item["dastvul_count"] for item in dastvul_rel_count_res},
        )
        has_vul_method_pool_set = set(VulMethodPool.objects.filter(vul_id__in=vul_ids).values_list("vul_id", flat=True))
        if vul_data:
            for item in vul_data:
                item["level_name"] = APP_LEVEL_RISK.get(str(item["level_id"]), "")
                item["server_type"] = VulSerializer.split_container_name(item["server__container"])
                item["is_header_vul"] = VulSerializer.judge_is_header_vul(item["strategy_id"])
                item["agent__project_name"] = item["project__name"]
                item["agent__server__container"] = item["server__container"]
                item["agent__language"] = item["language"]
                item["agent__bind_project_id"] = item["project_id"]
                item["header_vul_urls"] = VulSerializer.find_all_urls(item["id"]) if item["is_header_vul"] else []
                item["dastvul__vul_type"] = dast_vul_types_dict[item["id"]]
                item["dastvul_count"] = dastvul_rel_count_res_dict[item["id"]]
                item["dast_validation_status"] = bool(dastvul_rel_count_res_dict[item["id"]])
                item["has_vul_method_pool"] = item["id"] in has_vul_method_pool_set
                end["data"].append(item)
        # all Iast Vulnerability Status
        status = IastVulnerabilityStatus.objects.all()
        status_obj = {}
        for tmp_status in status:
            status_obj[tmp_status.id] = tmp_status.name
        for i in end["data"]:
            i["status__name"] = status_obj.get(i["status_id"], "")

        set_vul_inetration(end, request.user.id)
        return R.success(
            data={
                "messages": end["data"],
                "page": {"page_size": page_size, "cur_page": page},
            },
        )


def set_vul_inetration(end: dict[str, Any], user_id: int) -> None:
    pass


def get_vul_list_from_elastic_search(
    projects,
    project_ids=None,
    project_version_ids=None,
    hook_type_ids=None,
    level_ids=None,
    status_ids=None,
    strategy_ids=None,
    language_ids=None,
    search_keyword="",
    page=1,
    page_size=10,
    bind_project_id=0,
    project_version_id=0,
    order="",
):
    if project_ids is None:
        project_ids = []
    if project_version_ids is None:
        project_version_ids = []
    if hook_type_ids is None:
        hook_type_ids = []
    if level_ids is None:
        level_ids = []
    if status_ids is None:
        status_ids = []
    if strategy_ids is None:
        strategy_ids = []
    if language_ids is None:
        language_ids = []

    from dongtai_common.models.strategy import IastStrategyModel

    auth_project_ids = list(project_ids.values_list("id", flat=True))
    must_query = [
        Q("terms", bind_project_id=auth_project_ids),
        Q("terms", is_del=[0]),
        Q("range", bind_project_id={"gt": 0}),
        Q("range", strategy_id={"gt": 0}),
    ]
    order_list = ["_score", "level_id", "-latest_time", "-id"]
    if order:
        order_list.insert(0, order)
    if bind_project_id:
        must_query.append(Q("terms", bind_project_id=[bind_project_id]))
    if project_version_id:
        must_query.append(Q("terms", project_version_id=[project_version_id]))
    if project_ids:
        must_query.append(Q("terms", project_id=project_ids))
    if project_version_ids:
        must_query.append(Q("terms", project_version_id=project_version_ids))
    if level_ids:
        must_query.append(Q("terms", level_id=level_ids))
    if status_ids:
        must_query.append(Q("terms", status_id=status_ids))
    if language_ids:
        must_query.append(Q("terms", **{"language.keyword": language_ids}))
    if strategy_ids:
        must_query.append(Q("terms", strategy_id=strategy_ids))
    if search_keyword:
        must_query.append(
            Q(
                "multi_match",
                query=search_keyword,
                fields=[
                    "search_keywords",
                    "uri",
                    "vul_title",
                    "http_protocol",
                    "top_stack",
                    "bottom_stack",
                ],
            )
        )
    a = Q("bool", must=must_query)
    hashkey = make_hash(
        [
            auth_project_ids,
            project_ids,
            project_version_ids,
            hook_type_ids,
            level_ids,
            status_ids,
            language_ids,
            search_keyword,
            page_size,
            bind_project_id,
            project_version_id,
        ]
    )
    if page == 1:
        cache.delete(hashkey)
    after_table = cache.get(hashkey, {})
    after_key = after_table.get(page, None)
    extra_dict = {}
    if after_key:
        extra_dict["search_after"] = after_key
    res = (
        IastVulnerabilityDocument.search()
        .query(a)
        .extra(**extra_dict)
        .sort(*order_list)[:page_size]
        .using(Elasticsearch(settings.ELASTICSEARCH_DSL["default"]["hosts"]))
    )
    resp = res.execute()
    extra_datas = IastVulnerabilityModel.objects.filter(pk__in=[i["id"] for i in resp]).values(
        "strategy__vul_name",
        "language",
        "project__name",
        "server_id",
        "project_id",
        "id",
    )
    extra_data_dic = {ex_data["id"]: ex_data for ex_data in extra_datas}
    vuls = [i._d_ for i in list(resp)]
    vul_incorrect_id = []
    iast_vulnerability_values = (
        "language",
        "project__name",
        "server__container",
        "project_id",
        "id",
    )
    strategy_values = ("vul_name",)
    for vul in vuls:
        if "server__container" not in vul:
            vul["server__container"] = ""
        if vul["id"] not in extra_data_dic:
            vul_incorrect_id.append(vul["id"])
            strategy_dic = IastStrategyModel.objects.filter(pk=vul["strategy_id"]).values(*strategy_values).first()
            iast_vulnerability_dic = (
                IastVulnerabilityModel.objects.filter(pk=vul["agent_id"]).values(*iast_vulnerability_values).first()
            )
            if not strategy_dic:
                strategy_dic = {i: "" for i in strategy_values}
            if not iast_vulnerability_dic:
                iast_vulnerability_dic = {i: "" for i in iast_vulnerability_values}
            vul["agent__project_name"] = vul["project__name"]
            vul["agent__server__container"] = vul["server__container"]
            vul["agent__language"] = vul["language"]
            vul["agent__bind_project_id"] = vul["project_id"]
            for k, v in strategy_dic.items():
                vul["strategy__" + k] = v
            for k, v in iast_vulnerability_dic.items():
                vul["agent__" + k] = v
        else:
            vul.update(extra_data_dic[vul["id"]])
    if vul_incorrect_id:
        data_correction_interpetor.delay("vulnerablity_sync_fail")
    if resp.hits:
        afterkey = resp.hits[-1].meta["sort"]
        after_table[page + 1] = afterkey
        cache.set(hashkey, after_table)
    return vuls
