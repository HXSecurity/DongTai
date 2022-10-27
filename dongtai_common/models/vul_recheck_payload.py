from django.db import models
from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed
from time import time
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _
from dongtai_common.models.strategy import IastStrategyModel


from _typeshed import Incomplete
class IastVulRecheckPayload(models.Model):
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    strategy: Incomplete = models.ForeignKey(IastStrategyModel,
                                 models.DO_NOTHING,
                                 blank=True,
                                 null=True)
    value: Incomplete = models.CharField(blank=True, default=None, max_length=255)
    status: Incomplete = models.IntegerField(blank=True, default=None)
    create_time: Incomplete = models.IntegerField(default=lambda: int(time()),
                                      blank=True,
                                      null=True)
    language_id: Incomplete = models.IntegerField(blank=True, default=0)

    class Meta:
        db_table: str = 'iast_vul_recheck_payload'
