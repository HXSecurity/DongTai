import logging

from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.project import IastProject
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils.const import OPERATE_GET
from dongtai_conf.patch import patch_point, to_patch
from dongtai_conf.settings import ELASTICSEARCH_STATE
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from dongtai_web.utils import dict_transfrom, extend_schema_with_envcheck

logger = logging.getLogger("dongtai-webapi")


def _annotate_by_query(q, value_fields, count_field):
    return IastVulnerabilityModel.objects.filter(q).values(*value_fields).annotate(count=Count(count_field))


def get_annotate_cache_data(projects: QuerySet[IastProject]):
    return get_annotate_data(projects, 0, 0)


@to_patch
def get_annotate_data(projects: QuerySet[IastProject], bind_project_id: int, project_version_id: int) -> dict:
    cache_q = Q(is_del=0, project_id__gt=0, project__in=projects)

    # 从项目列表进入 绑定项目id
    if bind_project_id:
        cache_q = cache_q & Q(project_id=bind_project_id)
    # 项目版本号
    if project_version_id:
        cache_q = cache_q & Q(project_version_id=project_version_id)

    result_summary = {
        "level": [],
        "status": [],
        "hook_type": [],
        "language": [],
        "project": [],
    }

    cache_q, result_summary = patch_point(cache_q, result_summary)

    # 漏洞类型统计
    strategy_info = _annotate_by_query(cache_q, ("strategy_id", "strategy__vul_name"), "strategy_id")
    result_summary["hook_type"].extend(
        {
            "name": item["strategy__vul_name"],
            "num": item["count"],
            "id": item["strategy_id"],
        }
        for item in strategy_info
    )

    # 漏洞等级筛选
    count_info_level = _annotate_by_query(cache_q, ("level_id", "level__name_value"), "level_id")
    result_summary["level"].extend(
        {
            "name": item["level__name_value"],
            "num": item["count"],
            "id": item["level_id"],
        }
        for item in count_info_level
    )

    # # 按状态筛选
    status_info = _annotate_by_query(cache_q, ("status_id", "status__name"), "status_id")
    result_summary["status"].extend(
        {
            "name": item["status__name"],
            "num": item["count"],
            "id": item["status_id"],
        }
        for item in status_info
    )

    return result_summary


class GetAppVulsSummary(UserEndPoint):
    @extend_schema_with_envcheck(
        request=AggregationArgsSerializer,
        tags=[_("Vulnerability"), OPERATE_GET],
        summary="应用漏洞列表统计",
    )
    def post(self, request):
        """
        :param request:
        :return:
        """

        projects = request.user.get_projects()

        ser = AggregationArgsSerializer(data=request.data)
        bind_project_id = 0
        project_version_id = 0
        try:
            if ser.is_valid(True):
                if ser.validated_data.get("bind_project_id", 0):
                    bind_project_id = ser.validated_data.get("bind_project_id", 0)
                if ser.validated_data.get("project_version_id", 0):
                    project_version_id = ser.validated_data.get("project_version_id", 0)

            if ELASTICSEARCH_STATE:
                result_summary = get_annotate_data_es(projects, bind_project_id, project_version_id)
            elif bind_project_id or project_version_id:
                result_summary = get_annotate_data(projects, bind_project_id, project_version_id)
            else:
                # 全局下走缓存
                result_summary = get_annotate_cache_data(projects)
        except ValidationError as e:
            logger.info(e)
            return R.failure(data=e.detail)

        return R.success(
            data={
                "messages": result_summary,
            },
        )


@to_patch
def get_annotate_data_es(projects: QuerySet[IastProject], bind_project_id: int, project_version_id: int):
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import A, Q

    from dongtai_common.models.strategy import IastStrategyModel
    from dongtai_common.models.vul_level import IastVulLevel
    from dongtai_common.models.vulnerablity import (
        IastVulnerabilityDocument,
        IastVulnerabilityStatus,
    )

    strategy_ids = list(IastStrategyModel.objects.all().values_list("id", flat=True))

    must_query = [
        Q("terms", bind_project_id=list(projects.values_list("id", flat=True))),
        Q("terms", is_del=[0]),
        Q("terms", is_del=[0]),
        Q("range", bind_project_id={"gt": 0}),
        Q("range", strategy_id={"gt": 0}),
        Q("terms", strategy_id=strategy_ids),
    ]
    if bind_project_id:
        must_query.append(Q("terms", bind_project_id=[bind_project_id]))
    if project_version_id:
        must_query.append(Q("terms", project_version_id=[project_version_id]))
    search = IastVulnerabilityDocument.search().query(Q("bool", must=must_query))[:0]
    buckets = {
        "level": A("terms", field="level_id", size=2147483647),
        "strategy": A("terms", field="strategy_id", size=2147483647),
        "status": A("terms", field="status_id", size=2147483647),
    }
    buckets = patch_point(buckets)
    for k, v in buckets.items():
        search.aggs.bucket(k, v)
    from dongtai_conf import settings

    res = search.using(Elasticsearch(settings.ELASTICSEARCH_DSL["default"]["hosts"])).execute()
    dic = {}
    for key_ in buckets:
        key = key_
        origin_buckets = res.aggs[key].to_dict()["buckets"]
        for i in origin_buckets:
            i["id"] = i["key"]
            del i["key"]
            i["num"] = i["doc_count"]
            del i["doc_count"]
        if key == "strategy":
            strategy_ids = [i["id"] for i in origin_buckets]
            strategy = IastStrategyModel.objects.filter(pk__in=strategy_ids).values("id", "vul_name").all()
            strategy_dic = dict_transfrom(strategy, "id")
            for i in origin_buckets:
                i["name"] = strategy_dic[i["id"]]["vul_name"]
            key = "hook_type"
        if key == "status":
            status_ids = [i["id"] for i in origin_buckets]
            status = IastVulnerabilityStatus.objects.filter(pk__in=status_ids).values("id", "name").all()
            status_dic = dict_transfrom(status, "id")
            for i in origin_buckets:
                i["name"] = status_dic[i["id"]]["name"]
        if key == "level":
            level_ids = [i["id"] for i in origin_buckets]
            level = IastVulLevel.objects.filter(pk__in=level_ids).values("id", "name_value").all()
            level_dic = dict_transfrom(level, "id")
            for i in origin_buckets:
                i["name"] = level_dic[i["id"]]["name_value"]
            origin_buckets = sorted(origin_buckets, key=lambda x: x["id"])
        key, origin_buckets = patch_point(key, origin_buckets)
        dic[key] = list(origin_buckets)
    return dict(dic)
