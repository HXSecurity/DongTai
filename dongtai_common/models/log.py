from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed


class OperateType(models.IntegerChoices):
    GET = 1, _("GET")
    ADD = 2, _("ADD")
    CHANGE = 3, _("CHANGE")
    DELETE = 4, _("DELETE")


class IastLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    action_time = models.DateTimeField(
        _("action time"),
        default=timezone.now,
        editable=False,
    )
    url = models.CharField(max_length=255)
    raw_url = models.CharField(max_length=255)
    module_name = models.CharField(max_length=255)
    function_name = models.CharField(max_length=255)
    operate_type = models.IntegerField(choices=OperateType.choices)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    access_ip = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_log"
