######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : version_control
# @created     : 星期四 1月 20, 2022 17:32:43 CST
#
# @description :
######################################################################

import time
from django.db import models
from dongtai_common.utils.settings import get_managed


class VersionControl(models.Model):
    version = models.CharField(max_length=255, blank=True, null=True)
    component_name = models.CharField(max_length=255, blank=True, null=True)
    component_version_hash = models.CharField(max_length=255, blank=True, null=True)
    additional = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.IntegerField(default=lambda: int(time.time()), blank=True)

    class Meta:
        managed = get_managed()
        db_table = "project_version_control"
