from django.db import models
from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed
from time import time
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


# agent 阀值监控配置
class IastAgentConfig(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    details = models.JSONField()
    hostname = models.CharField(max_length=255, blank=True)
    ip = models.CharField(max_length=100, blank=True)
    port = models.IntegerField()
    cluster_name = models.CharField(max_length=255, blank=True)
    cluster_version = models.CharField(max_length=100, blank=True)
    priority = models.IntegerField()
    create_time = models.IntegerField()

    class Meta:
        managed = get_managed()
        db_table = "iast_agent_config"
        # agent 阀值监控配置


class TargetOperator(IntegerChoices):
    EQUAL = 1, _("等于")
    NOT_EQUAL = 2, _("不等于")
    CONTAIN = 3, _("包含")
    NOT_CONTAIN = 4, _("不包含")


class MetricOperator(IntegerChoices):
    GREATER = 5, _("大于")


class MetricGroup(IntegerChoices):
    SYSTEM = 1, _("性能指标")




class DealType(IntegerChoices):
    RELIVE = 2, _("恢复后启动")


class TargetType(IntegerChoices):
    ACCOUNT_NAME = 1, _("帐号")
    PROJECT_NAME = 2, _("项目名")
    PROTOCOL = 3, _("协议")
    AGENT_NAME = 4, _("Agent名称")
    AGENT_IP = 5, _("Agent IP")
    AGENT_PATH = 6, _("Agent 启动路径")
    PORT = 7, _("端口")
    AGENT_LANGUAGE = 8, _("语言")


# keep match with agent ,ignore its naming style
class MetricType(IntegerChoices):
    cpuUsagePercentage = 1, _("系统CPU使用率阈值")
    sysMemUsagePercentage = 2, _("系统内存使用率阈值")




UNIT_DICT = {
    1: "%",
    2: "%",
    3: "kb",
    4: "%",
    5: "kb",
    6: "个",
    7: "个",
    8: "个",
    9: "次",
    10: "次",
    11: "ms",
}


class SystemMetricType(IntegerChoices):
    cpuUsagePercentage = 1, _("系统CPU使用率阈值")
    sysMemUsagePercentage = 2, _("系统内存使用率阈值")




class JVMMetricType(IntegerChoices):
    pass




class ApplicationMetricType(IntegerChoices):
    pass




class IastCircuitConfig(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=200, blank=True)
    metric_types = models.CharField(max_length=2000, blank=True)
    target_types = models.CharField(max_length=2000, blank=True, db_column="targets")
    system_type = models.IntegerField(blank=True, null=True)
    is_enable = models.IntegerField()
    is_deleted = models.IntegerField(default=0)
    deal = models.IntegerField()
    interval = models.IntegerField(default=30)
    metric_group = models.IntegerField()
    priority = models.IntegerField()
    create_time = models.IntegerField(blank=True, default=lambda: int(time()))
    update_time = models.IntegerField(blank=True, default=lambda: int(time()))

    class Meta:
        managed = get_managed()
        db_table = "iast_circuit_configs"


class IastCircuitTarget(models.Model):
    circuit_config = models.ForeignKey(IastCircuitConfig, on_delete=models.CASCADE)
    target_type = models.IntegerField()
    opt = models.IntegerField()
    value = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_circuit_targets"


class IastCircuitMetric(models.Model):
    circuit_config = models.ForeignKey(IastCircuitConfig, on_delete=models.CASCADE)
    metric_type = models.IntegerField()
    opt = models.IntegerField()
    value = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_circuit_metrics"
