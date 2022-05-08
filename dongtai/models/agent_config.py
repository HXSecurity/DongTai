from django.db import models
from dongtai.models import User
from dongtai.utils.settings import get_managed
from time import time
from django.db.models import IntegerChoices

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
        # agent 阀值监控配置

class Operator(IntegerChoices):
    EQUAL = 1
    NOT_EQUAL = 2
    CONTAIN = 3
    NOT_CONTAIN = 4
    GREATER = 5


class MetricGroup(IntegerChoices):
    SYSTEM = 1
    JVM = 2
    APPLICATION = 3

class DealType(IntegerChoices):
    UNLOAD = 1
    RELIVE = 2


class TargetType(IntegerChoices):
    ACCOUNT_NAME = 1
    PROJECT_NAME = 2
    PROTOCOL = 3
    AGENT_NAME = 4
    AGENT_IP = 5
    AGENT_PATH = 6
    PORT = 7
    AGENT_LANGUAGE = 8


#keep match with agent ,ignore its naming style
class MetricType(IntegerChoices):
    cpuUsagePercentage = 1
    sysMemUsagePercentage = 2
    sysMemUsageUsed = 3
    jvmMemUsagePercentage = 4
    jvmMemUsageUsed = 5
    threadCount = 6
    daemonThreadCount = 7
    dongTaiThreadCount = 8
    hookLimitTokenPerSecond = 9
    heavyTrafficLimitTokenPerSecond = 10

class IastCircuitConfig(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=200, blank=True, null=True)
    metric_types = models.CharField(max_length=2000, blank=True, null=True)
    targets = models.CharField(max_length=2000, blank=True, null=True)
    system_type = models.IntegerField(blank=True, null=True)
    is_enable = models.IntegerField(blank=True, null=True)
    is_deleted = models.IntegerField(default=0, blank=True, null=True)
    deal = models.IntegerField(blank=True, null=True)
    interval = models.IntegerField(blank=True, null=True)
    metric_group = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True,
                                      null=True,
                                      default=int(time()))
    update_time = models.IntegerField(blank=True,
                                      null=True,
                                      default=int(time()))

    class Meta:
        managed = get_managed()
        db_table = 'iast_circuit_configs'


class IastCircuitTarget(models.Model):
    circuit_config = models.ForeignKey(IastCircuitConfig,
                                       on_delete=models.CASCADE)
    target_type = models.IntegerField(blank=True, null=True)
    opt = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_circuit_targets'


class IastCircuitMetric(models.Model):
    circuit_config = models.ForeignKey(IastCircuitConfig,
                                       on_delete=models.CASCADE)
    metric_type = models.IntegerField(blank=True, null=True)
    opt = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_circuit_metrics'
