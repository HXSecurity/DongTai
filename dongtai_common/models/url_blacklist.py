from django.db import models
from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _
from time import time
from typing import List, Dict

class TargetOperator(IntegerChoices):
    #    EQUAL = 1, _("等于")
    #    NOT_EQUAL = 2, _("不等于")
    CONTAIN = 3, _("包含")
    NOT_CONTAIN = 4, _("不包含")
    KEY_CONTAIN = 6, _("不包含")
    VALUE_CONTAIN = 5, _("不包含")


class TargetType(IntegerChoices):
    URL = 1, _("URL")
    HEADER = 2, _("Header")


class TargetScope(IntegerChoices):
    GLOBAL = 1, _("GLOBAL")


class IastAgentBlackRule(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    target_type = models.IntegerField(
        choices=TargetType,
        blank=True,
        null=True,
    )
    scope = models.IntegerField(
        choices=TargetScope,
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
    rule = models.ForeignKey(IastAgentBlackRule, models.DO_NOTHING)
    operator = models.IntegerField(choices=TargetOperator,
                                   blank=True,
                                   null=True)
    value = models.CharField(max_length=512, default="", null=False)
    create_time = models.DateTimeField(
        blank=True,
        null=True,
        auto_now_add=True,
    )
    update_time = models.DateTimeField(
        blank=True,
        null=True,
        auto_now=True,
    )

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent_black_rule_detail'

    def to_agent_rule(self) -> Dict:
        return {self.operator: self.value}
