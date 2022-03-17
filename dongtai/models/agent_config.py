from django.db import models
from dongtai.models import User
from dongtai.utils.settings import get_managed


# agent 阀值监控配置
class IastAgentConfig(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    details = models.JSONField()
    hostname = models.CharField(max_length=255, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    cluster_name = models.CharField(max_length=255, blank=True, null=True)
    cluster_version = models.CharField(max_length=100, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent_config'
