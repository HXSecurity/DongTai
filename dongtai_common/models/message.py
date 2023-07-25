######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : message
# @created     : 星期三 10月 13, 2021 12:09:11 CST
#
# @description :
######################################################################


from django.db import models

from dongtai_common.utils.db import get_timestamp
from dongtai_common.utils.settings import get_managed


class IastMessageType(models.Model):
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_message_type"


class IastMessage(models.Model):
    message = models.CharField(max_length=512, blank=True)
    relative_url = models.CharField(max_length=512, blank=True)
    create_time = models.IntegerField(default=get_timestamp)
    read_time = models.IntegerField(default=0)
    is_read = models.IntegerField(default=0)
    message_type = models.ForeignKey(
        IastMessageType,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column="message_type_id",
    )
    to_user_id = models.IntegerField(default=0)

    class Meta:
        managed = get_managed()
        db_table = "iast_message"
