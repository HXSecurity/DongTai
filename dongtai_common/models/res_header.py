######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : res_header
# @created     : 星期三 1月 12, 2022 16:49:40 CST
#
# @description :
######################################################################


from django.db import models
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.agent import IastAgent


from _typeshed import Incomplete
class HeaderType(models.IntegerChoices):
    REQUEST: int = 1
    RESPONSE: int = 2


class ProjectSaasMethodPoolHeader(models.Model):
    key: Incomplete = models.CharField(max_length=255, blank=True, null=False)
    agent: Incomplete = models.ForeignKey(IastAgent,
                              models.DO_NOTHING,
                              blank=True,
                              null=True,
                              db_constraint=False)
    header_type: Incomplete = models.IntegerField(choices=HeaderType.choices,default=0)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_project_header'
