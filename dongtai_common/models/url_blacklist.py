from django.db import models
from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _
from typing import List, Dict


class TargetOperator(IntegerChoices):
    EQUAL = 1, _("等于")
    NOT_EQUAL = 2, _("不等于")
    CONTAIN = 3, _("包含")
    NOT_CONTAIN = 4, _("不包含")
    EXISTS = 5, _("存在")
    NOT_EXISTS = 6, _("不存在")


class TargetType(IntegerChoices):
    URL = 1, _("URL")
    HEADER_KEY = 2, _("Header Key")


class TargetScope(IntegerChoices):
    GLOBAL = 1, _("GLOBAL")
    TEMPLATE = 2, _("TEMPLATE")
    PROJECT = 3, _("PROJECT")


class State(IntegerChoices):
    ENABLE = 1, _("ENABLE")
    DISABLE = 2, _("DISABLE")


class IastAgentBlackRule(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    scope = models.IntegerField(
        choices=TargetScope.choices,
        blank=True,
        null=True,
        default=TargetScope.GLOBAL,
    )
    state = models.IntegerField(
        choices=State.choices,
        blank=True,
        null=True,
    )

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent_black_rule'

    def to_full_rule(self) -> List[Dict]:
        return list(
            map(lambda x: x.to_agent_rule(),
                self.iastagentblackruledetail_set.all()))


class IastAgentBlackRuleDetail(models.Model):
    target_type = models.IntegerField(choices=TargetType.choices)
    rule = models.ForeignKey(IastAgentBlackRule, models.DO_NOTHING)
    operator = models.IntegerField(choices=TargetOperator.choices)
    value = models.CharField(max_length=512, default="", null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent_black_rule_detail'

    def to_agent_rule(self) -> Dict:
        return {
            'target_type': TargetType(self.target_type).name,
            'operator': TargetOperator(self.operator).name,
            'value': self.value,
        }


def create_blacklist_rule(target_type: TargetType, operator: TargetOperator,
                          value: str, user_id: int, state: State):
    ruledetail = IastAgentBlackRuleDetail.objects.create(
        target_type=target_type, operator=operator, value=value)
    rule = IastAgentBlackRule.objects.create(user_id=user_id, state=state)
    ruledetail.rule = rule
    ruledetail.save()
