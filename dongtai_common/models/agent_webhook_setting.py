from django.db import models
from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed


# agent report static forward by type
from _typeshed import Incomplete
class IastAgentUploadTypeUrl(models.Model):
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING)
    type_id: Incomplete = models.IntegerField(blank=True, null=True)
    send_num: Incomplete = models.IntegerField(blank=True, null=True,default=0)
    url: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    headers: Incomplete = models.JSONField()

    create_time: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_agent_upload_type_url'
