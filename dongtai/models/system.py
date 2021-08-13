from django.db import models

from dongtai.models import User
import os


class IastSystem(models.Model):
    id = models.BigAutoField(primary_key=True)
    agent_value = models.CharField(max_length=50, blank=True, null=True)
    java_version = models.CharField(max_length=50, blank=True, null=True)
    middleware = models.CharField(max_length=50, blank=True, null=True)
    system = models.CharField(max_length=50, blank=True, null=True)
    deploy_status = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField( auto_now_add=True)
    update_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True if os.getenv('environment',None) == 'TEST' else False
        db_table = 'iast_system'
