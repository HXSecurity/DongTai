from django.db import models

from dongtai_common.utils.settings import get_managed


class IastWebHookLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_type = models.CharField(max_length=255)
    body = models.JSONField()
    create_time = models.IntegerField()

    class Meta:
        managed = get_managed()
        db_table = "iast_webhook_log"
