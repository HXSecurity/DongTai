from django.db import models
from dongtai_common.models.project import IastProject
from django.db.models import IntegerChoices
from dongtai_common.utils.settings import get_managed


class RuleTypeChoices(models.IntegerChoices):
    BLACK = 1
    WHITE = 2


class IastRecognizeRule(models.Model):
    project = models.ForeignKey(IastProject,
                                on_delete=models.DO_NOTHING,
                                blank=True,
                                null=True,
                                default=-1,
                                db_constraint=False)
    rule_detail = models.CharField(max_length=255,
                                   default='',
                                   blank=True,
                                   null=True)
    rule_type = models.IntegerField(choices=RuleTypeChoices.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_recoginze_rule'
