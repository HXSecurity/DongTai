from django.db import models

from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastSystem(models.Model):
    id: Incomplete = models.BigAutoField(primary_key=True)
    agent_value: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    java_version: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    middleware: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    system: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    deploy_status: Incomplete = models.IntegerField(blank=True, null=True)
    created_at: Incomplete = models.DateTimeField(auto_now_add=True)
    update_at: Incomplete = models.DateTimeField(blank=True, null=True)
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_system'
