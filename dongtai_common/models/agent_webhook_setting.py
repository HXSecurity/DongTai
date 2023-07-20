from django.db import models

from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed


# agent report static forward by type
class IastAgentUploadTypeUrl(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    type_id = models.IntegerField(blank=True, null=True)
    send_num = models.IntegerField(blank=True, null=True, default=0)
    url = models.CharField(max_length=255, blank=True, null=True)
    headers = models.JSONField()

    create_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_agent_upload_type_url"
