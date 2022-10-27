######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : engine_monitoring_indicators
# @created     : Wednesday Aug 25, 2021 14:51:16 CST
#
# @description :
######################################################################

from django.db import models
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastEnginMonitoringIndicators(models.Model):
    key: Incomplete = models.CharField(max_length=100,
                           blank=True,
                           default='',
                           null=False,
                           unique=True)
    name: Incomplete = models.CharField(max_length=100, blank=True, default='', null=False)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'engine_monitoring_indicators'
