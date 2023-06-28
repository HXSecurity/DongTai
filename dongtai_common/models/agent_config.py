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
    hostname = models.CharField(max_length=255, )
    ip = models.CharField(max_length=100, )
    port = models.IntegerField()
    cluster_name = models.CharField(max_length=255, )
    cluster_version = models.CharField(max_length=100, )
    priority = models.IntegerField()
    create_time = models.IntegerField()

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent_config'
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
#    JVM = 2, _("JVM指标")
#    APPLICATION = 3, _("应用指标")


class DealType(IntegerChoices):
    #    UNLOAD = 1, _("完全卸载")
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
#    sysMemUsageUsed = 3, _("系统内存使用值阈值")
#    jvmMemUsagePercentage = 4, _("JVM内存使用率阈值")
#    jvmMemUsageUsed = 5, _("JVM内存使用值阈值")
#    threadCount = 6, _("总线程数阈值")
#    daemonThreadCount = 7, _("守护线程数阈值")
#    dongTaiThreadCount = 8, _("洞态IAST线程数阈值")
#    hookLimitTokenPerSecond = 9, _("单请求HOOK限流")
#    heavyTrafficLimitTokenPerSecond = 10, _("每秒限制处理请求数量（QPS）")
#    apiResponseTime = 11, _("请求响应时间阈值")


UNIT_DICT = {
    1: "%",
    2: "%",
    3: "kb",
    4: "%",
    5: "kb",
    6: "个",
    6: "个",
    7: "个",
    8: "个",
    9: "次",
    10: '次',
    11: 'ms',
}


class SystemMetricType(IntegerChoices):
    cpuUsagePercentage = 1, _("系统CPU使用率阈值")
    sysMemUsagePercentage = 2, _("系统内存使用率阈值")
#    sysMemUsageUsed = 3, _("系统内存使用值阈值")


class JVMMetricType(IntegerChoices):
    pass
#    jvmMemUsagePercentage = 4, _("JVM内存使用率阈值")
#    jvmMemUsageUsed = 5, _("JVM内存使用值阈值")
#    threadCount = 6, _("总线程数阈值")
#    daemonThreadCount = 7, _("守护线程数阈值")
#    dongTaiThreadCount = 8, _("洞态IAST线程数阈值")


class ApplicationMetricType(IntegerChoices):
    pass
#    hookLimitTokenPerSecond = 9, _("单请求HOOK限流")
#    heavyTrafficLimitTokenPerSecond = 10, _("每秒限制处理请求数量（QPS）")
#    apiResponseTime = 11, _("请求响应时间阈值")


class IastCircuitConfig(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=200, )
    metric_types = models.CharField(max_length=2000, )
    target_types = models.CharField(max_length=2000,
                                    blank=True,
                                    null=True,
                                    db_column='targets')
    system_type = models.IntegerField(blank=True, null=True)
    is_enable = models.IntegerField()
    is_deleted = models.IntegerField(default=0, )
    deal = models.IntegerField()
    interval = models.IntegerField(default=30)
    metric_group = models.IntegerField()
    priority = models.IntegerField()
    create_time = models.IntegerField(blank=True,
                                      null=True,
                                      default=lambda: int(time()))
    update_time = models.IntegerField(blank=True,
                                      null=True,
                                      default=lambda: int(time()))

    class Meta:
        managed = get_managed()
        db_table = 'iast_circuit_configs'


class IastCircuitTarget(models.Model):
    circuit_config = models.ForeignKey(IastCircuitConfig,
                                       on_delete=models.CASCADE)
    target_type = models.IntegerField()
    opt = models.IntegerField()
    value = models.CharField(max_length=200, )

    class Meta:
        managed = get_managed()
        db_table = 'iast_circuit_targets'


class IastCircuitMetric(models.Model):
    circuit_config = models.ForeignKey(IastCircuitConfig,
                                       on_delete=models.CASCADE)
    metric_type = models.IntegerField()
    opt = models.IntegerField()
    value = models.CharField(max_length=200, )

    class Meta:
        managed = get_managed()
        db_table = 'iast_circuit_metrics'
