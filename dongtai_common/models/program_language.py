######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : program_language
# @created     : Tuesday Sep 07, 2021 10:21:33 CST
#
# @description : 
######################################################################



from django.db import models
from dongtai_common.utils.settings import get_managed

from _typeshed import Incomplete
class IastProgramLanguage(models.Model):
    name: Incomplete = models.CharField(max_length=255, blank=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_program_language'
