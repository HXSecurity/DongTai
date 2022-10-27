######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : sensitive_info
# @created     : 星期五 11月 19, 2021 11:02:19 CST
#
# @description :
######################################################################

from django.db import models
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.user import User
import time


from _typeshed import Incomplete
class IastPatternType(models.Model):
    name: Incomplete = models.CharField(blank=True, default=None, max_length=255)
    id: Incomplete = models.IntegerField(default=0, db_column='value')
    logi_id: Incomplete = models.BigAutoField(primary_key=True, db_column='id')

    class Meta:
        db_table: str = 'iast_pattern_type'


class IastSensitiveInfoRule(models.Model):
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    strategy: Incomplete = models.ForeignKey(IastStrategyModel,
                                 models.DO_NOTHING,
                                 blank=True,
                                 null=True)
    pattern_type: Incomplete = models.ForeignKey(IastPatternType,
                                     models.DO_NOTHING,
                                     blank=True,
                                     default=None)
    pattern: Incomplete = models.CharField(blank=True, default=None, max_length=255)
    status: Incomplete = models.IntegerField(blank=True, default=None)
    latest_time: Incomplete = models.IntegerField(default=lambda: int(time.time()),
                                      blank=True,
                                      null=True)

    class Meta:
        db_table: str = 'iast_sensitive_info_rule'
