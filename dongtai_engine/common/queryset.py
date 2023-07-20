from dongtai_common.common.utils import cached_decorator
from dongtai_common.models.strategy_user import IastStrategyUser
from django.db.models import Sum, Q
from celery.apps.worker import logger
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.project import IastProject
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.hook_strategy import HookStrategy

LANGUAGE_MAP = {"JAVA": 1, "PYTHON": 2, "PHP": 3, "GO": 4}


@cached_decorator(random_range=(60, 120), use_celery_update=False)
def get_scan_id(project_id) -> int:
    res = IastProject.objects.filter(pk=project_id).values("scan_id").first()
    return res["scan_id"] if res else 0


@cached_decorator(random_range=(60, 120), use_celery_update=False)
def load_sink_strategy(user=None, language=None, scan_id=0) -> list[dict]:
    """
    加载用户user有权限方法的策略
    :param user: edit by song
    :return:
    """
    logger.info("start load sink_strategy")
    strategies = []
    language_id = 0
    if language and language in LANGUAGE_MAP:
        language_id = LANGUAGE_MAP[language]
    q = Q(state="enable")
    scan_template = IastStrategyUser.objects.filter(pk=scan_id).first()
    if scan_template:
        strategy_id = [int(i) for i in scan_template.content.split(",")]
        q = q & Q(pk__in=strategy_id)
    type_query = IastStrategyModel.objects.filter(q)
    strategy_models = HookStrategy.objects.filter(
        strategy__in=type_query,
        language_id__in=[language_id] if language_id else LANGUAGE_MAP.values(),
    ).values(
        "id",
        "value",
        "strategy__vul_type",
        "strategy__level",
        "strategy__vul_name",
        "strategy_id",
    )
    sub_method_signatures = set()
    for strategy in strategy_models:
        # for strategy in sub_queryset:
        strategy_value = strategy.get("value", "")
        sub_method_signature = (
            strategy_value[: strategy_value.rfind("(")]
            if strategy_value.rfind("(") > 0
            else strategy_value
        )
        if sub_method_signature in sub_method_signatures:
            continue
        sub_method_signatures.add(sub_method_signature)
        strategies.append(
            {
                "strategy": strategy.get("id", ""),
                "type": strategy.get("strategy__vul_type", ""),
                "value": sub_method_signature,
                "strategy_level": strategy.get("strategy__level"),
                "strategy_vul_name": strategy.get("strategy__vul_name"),
                "strategy_strategy_id": strategy.get("strategy_id"),
            }
        )
    return strategies


@cached_decorator(random_range=(60, 120), use_celery_update=False)
def get_agent(agent_id):
    return IastAgent.objects.filter(pk=agent_id).first()
