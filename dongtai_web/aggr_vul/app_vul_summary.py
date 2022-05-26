from rest_framework.serializers import ValidationError
from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.vulnerablity import IastVulnerabilityModel
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from dongtai.models import LANGUAGE_DICT
from dongtai_web.aggregation.aggregation_common import auth_user_list_str
from django.db.models import Count
from utils import cached_decorator
from django.db.models import Q


def _annotate_by_query(q, value_fields, count_field):
    return (
        IastVulnerabilityModel.objects.filter(q)
        .values(*value_fields)
        .annotate(count=Count(count_field))
    )

@cached_decorator(random_range=(2 * 60 * 60, 2 * 60 * 60),
                  use_celery_update=True)
def get_annotate_cache_data(user_id: int):
    return get_annotate_data(user_id, 0, 0)


def get_annotate_data(
    user_id: int, bind_project_id=int, project_version_id=int
) -> dict:
    auth_user_info = auth_user_list_str(user_id=user_id)
    cache_q = Q(is_del=0, agent__user_id__in=auth_user_info['user_list'])

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
    for item in language_info:
        result_summary["language"].append(
            {
                "name": item["agent__language"],
                "num": item["count"],
                "id": LANGUAGE_DICT.get(item["agent__language"]),
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
                if ser.validated_data.get("bind_project_id", 0):
                    bind_project_id = ser.validated_data.get("bind_project_id", 0)

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
