from rest_framework.serializers import ValidationError
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from dongtai_common.models import LANGUAGE_DICT
from dongtai_web.aggregation.aggregation_common import auth_user_list_str
from django.db.models import Count
from dongtai_common.common.utils import cached_decorator
from django.db.models import Q
import copy

def _annotate_by_query(q, value_fields, count_field):
    return (
        IastVulnerabilityModel.objects.filter(q)
        .values(*value_fields)
        .annotate(count=Count(count_field))
    )

#@cached_decorator(random_range=(2 * 60 * 60, 2 * 60 * 60),
#                  use_celery_update=True)
def get_annotate_cache_data(user_id: int):
    return get_annotate_data(user_id, 0, 0)


def get_annotate_data(
    user_id: int, bind_project_id=int, project_version_id=int
) -> dict:
    auth_user_info = auth_user_list_str(user_id=user_id)
    cache_q = Q(is_del=0,agent__bind_project_id__gt=0, agent__user_id__in=auth_user_info['user_list'])

    # 从项目列表进入 绑定项目id
    if bind_project_id:
        cache_q = cache_q & Q(agent__bind_project_id=bind_project_id)
    # 项目版本号
    if project_version_id:
        cache_q = cache_q & Q(agent__project_version_id=project_version_id)
    # 项目统计
    pro_info = _annotate_by_query(
        cache_q,
        ("agent__bind_project_id", "agent__project_name"),
        "agent__bind_project_id",
    )

    result_summary = {
        "level": [],
        "status": [],
        "hook_type": [],
        "language": [],
        "project": [],
    }

    for item in pro_info:
        result_summary["project"].append(
            {
                "name": item["agent__project_name"],
                "num": item["count"],
                "id": item["agent__bind_project_id"],
            }
        )
    # 漏洞类型统计
    strategy_info = _annotate_by_query(
        cache_q, ("strategy_id", "strategy__vul_name"), "strategy_id"
    )
    for item in strategy_info:
        result_summary["hook_type"].append(
            {
                "name": item["strategy__vul_name"],
                "num": item["count"],
                "id": item["strategy_id"],
            }
        )

    # 漏洞等级筛选
    count_info_level = _annotate_by_query(
        cache_q, ("level_id", "level__name_value"), "level_id"
    )
    for item in count_info_level:
        result_summary["level"].append(
            {
                "name": item["level__name_value"],
                "num": item["count"],
                "id": item["level_id"],
            }
        )

    # # 按状态筛选
    status_info = _annotate_by_query(
        cache_q, ("status_id", "status__name"), "status_id"
    )
    for item in status_info:
        result_summary["status"].append(
            {
                "name": item["status__name"],
                "num": item["count"],
                "id": item["status_id"],
            }
        )

    # # 按语言筛选
    language_info = _annotate_by_query(cache_q, ("agent__language",), "agent__language")
    lang_arr = copy.copy(LANGUAGE_DICT)
    lang_key = lang_arr.keys()
    for item in language_info:
        result_summary["language"].append(
            {
                "name": item["agent__language"],
                "num": item["count"],
                "id": lang_arr.get(item["agent__language"]),
            }
        )
        if item["agent__language"] in lang_key:
            del lang_arr[item["agent__language"]]
    if lang_arr:
        for item in lang_arr.keys():
            result_summary["language"].append(
                {
                    "name": item,
                    "num": 0,
                    "id": LANGUAGE_DICT.get(item),
                }
            )
    return result_summary


class GetAppVulsSummary(UserEndPoint):
    @extend_schema_with_envcheck(
        request=AggregationArgsSerializer,
        tags=[_("app Vul count")],
        summary=_("app List count"),
        description=_("select   app vul by keywords"),
    )
    def post(self, request):
        """
        :param request:
        :return:
        """

        user = request.user
        user_id = user.id

        ser = AggregationArgsSerializer(data=request.data)
        bind_project_id = 0
        project_version_id = 0
        try:
            if ser.is_valid(True):
                if ser.validated_data.get("bind_project_id", 0):
                    bind_project_id = ser.validated_data.get("bind_project_id", 0)
                if ser.validated_data.get("project_version_id", 0):
                    project_version_id = ser.validated_data.get("project_version_id", 0)

            if bind_project_id or project_version_id:
                result_summary = get_annotate_data(
                    user_id, bind_project_id, project_version_id
                )
            else:
                # 全局下走缓存
                result_summary = get_annotate_cache_data(user_id)
        except ValidationError as e:
            return R.failure(data=e.detail)

        return R.success(
            data={
                "messages": result_summary,
            },
        )

def get_annotate_data_es(user_id, bind_project_id, project_version_id):
    from dongtai_common.models.vulnerablity import IastVulnerabilityDocument
    from elasticsearch_dsl import Q, Search
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import A
    user_id_list = [user_id]
    must_query = [
        Q('terms', user_id=user_id_list),
        Q('terms', bind_project_id=[bind_project_id]),
        Q('terms', project_version_id=[project_version_id])
    ]
    search = IastVulnerabilityDocument.search().query(Q('bool', must=must_query))[:0]
    buckets = {
        'level_count': A('terms', field='level_id', size=2147483647),
        'project_count': A('terms', field='bind_project_id', size=2147483647),
        "strategy_count": A('terms', field='strategy_id', size=2147483647),
        'status_count': A('terms', field='status_id', size=2147483647),
        "language_count": A('terms', field='language.keyword', size=2147483647)
    }
    for k, v in buckets.items():
        search.aggs.bucket(k, v)
    from dongtai_conf import settings
    res = search.using(Elasticsearch(
        settings.ELASTICSEARCH_DSL['default']['hosts'])).execute()
    dic = {}
    for key in buckets.keys():
        origin_buckets = res.aggs[key]['buckets']
        for i in origin_buckets:
            i['id'] = i['key']
            del ['key']
        if key == 'strategy_count':
            strategy_ids = [i['id'] for i in origin_buckets]
            strategy = IastStrategyModel.objects.filter(
                pk__in=strategy_ids).all()
        dic[key] = origin_buckets
    return dic
