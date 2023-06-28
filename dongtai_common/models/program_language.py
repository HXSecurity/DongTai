######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : program_language
# @created     : Tuesday Sep 07, 2021 10:21:33 CST
#
# @description :
######################################################################


from django.db import models
from dongtai_common.utils.settings import get_managed


class IastProgramLanguage(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = get_managed()
        db_table = 'iast_program_language'
