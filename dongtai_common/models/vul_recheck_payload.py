
from django.db import models

from dongtai_common.models import User
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.utils.db import get_timestamp


class IastVulRecheckPayload(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    strategy = models.ForeignKey(IastStrategyModel, models.DO_NOTHING, blank=True, null=True)
    value = models.CharField(blank=True, default=None, max_length=255)
    status = models.IntegerField(blank=True, default=None)
    create_time = models.IntegerField(default=get_timestamp, blank=True, null=True)
    language_id = models.IntegerField(blank=True, default=0)

    class Meta:
        db_table = "iast_vul_recheck_payload"
