######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : message
# @created     : 星期三 10月 13, 2021 12:09:11 CST
#
# @description :
######################################################################


from django.db import models
from dongtai_common.utils.settings import get_managed
from time import time

from _typeshed import Incomplete
class IastMessageType(models.Model):
    name: Incomplete = models.CharField(max_length=100, blank=True, null=False, default='')

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_message_type'


class IastMessage(models.Model):
    message: Incomplete = models.CharField(max_length=512,
                               blank=True,
                               null=False,
                               default='')
    relative_url: Incomplete = models.CharField(max_length=512,
                                    blank=True,
                                    null=False,
                                    default='')
    create_time: Incomplete = models.IntegerField(blank=True, default=lambda: int(time()))
    read_time: Incomplete = models.IntegerField(blank=True, default=0)
    is_read: Incomplete = models.IntegerField(blank=True, null=True, default=0)
    message_type: Incomplete = models.ForeignKey(IastMessageType,
                                     on_delete=models.DO_NOTHING,
                                     db_constraint=False,
                                     db_column='message_type_id')
    to_user_id: Incomplete = models.IntegerField(default=0)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_message'
