from django.db import models
from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed
from time import time
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


# agent 阀值监控配置
from _typeshed import Incomplete
class IastAgentConfig(models.Model):
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING)
    details: Incomplete = models.JSONField()
    hostname: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    ip: Incomplete = models.CharField(max_length=100, blank=True, null=True)
    port: Incomplete = models.IntegerField(blank=True, null=True)
    cluster_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    cluster_version: Incomplete = models.CharField(max_length=100, blank=True, null=True)
    priority: Incomplete = models.IntegerField(blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_agent_config'
        # agent 阀值监控配置


class TargetOperator(IntegerChoices):
    EQUAL: Incomplete = 1, _("等于")
    NOT_EQUAL: Incomplete = 2, _("不等于")
    CONTAIN: Incomplete = 3, _("包含")
    NOT_CONTAIN: Incomplete = 4, _("不包含")


class MetricOperator(IntegerChoices):
    GREATER: Incomplete = 5, _("大于")


class MetricGroup(IntegerChoices):
    SYSTEM: Incomplete = 1, _("性能指标")
    JVM: Incomplete = 2, _("JVM指标")
    APPLICATION: Incomplete = 3, _("应用指标")


class DealType(IntegerChoices):
    UNLOAD: Incomplete = 1, _("完全卸载")
    RELIVE: Incomplete = 2, _("恢复后启动")


class TargetType(IntegerChoices):
    ACCOUNT_NAME: Incomplete = 1, _("帐号")
    PROJECT_NAME: Incomplete = 2, _("项目名")
    PROTOCOL: Incomplete = 3, _("协议")
    AGENT_NAME: Incomplete = 4, _("Agent名称")
    AGENT_IP: Incomplete = 5, _("Agent IP")
    AGENT_PATH: Incomplete = 6, _("Agent 启动路径")
    PORT: Incomplete = 7, _("端口")
    AGENT_LANGUAGE: Incomplete = 8, _("语言")


#keep match with agent ,ignore its naming style
class MetricType(IntegerChoices):
    cpuUsagePercentage: Incomplete = 1, _("系统CPU使用率阈值")
    sysMemUsagePercentage: Incomplete = 2, _("系统内存使用率阈值")
    sysMemUsageUsed: Incomplete = 3, _("系统内存使用值阈值")
    jvmMemUsagePercentage: Incomplete = 4, _("JVM内存使用率阈值")
    jvmMemUsageUsed: Incomplete = 5, _("JVM内存使用值阈值")
    threadCount: Incomplete = 6, _("总线程数阈值")
    daemonThreadCount: Incomplete = 7, _("守护线程数阈值")
    dongTaiThreadCount: Incomplete = 8, _("洞态IAST线程数阈值")
    hookLimitTokenPerSecond: Incomplete = 9, _("单请求HOOK限流")
    heavyTrafficLimitTokenPerSecond: Incomplete = 10, _("每秒限制处理请求数量（QPS）")
    apiResponseTime: Incomplete = 11, _("请求响应时间阈值")


UNIT_DICT: Incomplete = {
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
    cpuUsagePercentage: Incomplete = 1, _("系统CPU使用率阈值")
    sysMemUsagePercentage: Incomplete = 2, _("系统内存使用率阈值")
    sysMemUsageUsed: Incomplete = 3, _("系统内存使用值阈值")


class JVMMetricType(IntegerChoices):
    jvmMemUsagePercentage: Incomplete = 4, _("JVM内存使用率阈值")
    jvmMemUsageUsed: Incomplete = 5, _("JVM内存使用值阈值")
    threadCount: Incomplete = 6, _("总线程数阈值")
    daemonThreadCount: Incomplete = 7, _("守护线程数阈值")
    dongTaiThreadCount: Incomplete = 8, _("洞态IAST线程数阈值")


class ApplicationMetricType(IntegerChoices):
    hookLimitTokenPerSecond: Incomplete = 9, _("单请求HOOK限流")
    heavyTrafficLimitTokenPerSecond: Incomplete = 10, _("每秒限制处理请求数量（QPS）")
    apiResponseTime: Incomplete = 11, _("请求响应时间阈值")


class IastCircuitConfig(models.Model):
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING)
    name: Incomplete = models.CharField(max_length=200, blank=True, null=True)
    metric_types: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    target_types: Incomplete = models.CharField(max_length=2000,
                                    blank=True,
                                    null=True,
                                    db_column='targets')
    system_type: Incomplete = models.IntegerField(blank=True, null=True)
    is_enable: Incomplete = models.IntegerField(blank=True, null=True)
    is_deleted: Incomplete = models.IntegerField(default=0, blank=True, null=True)
    deal: Incomplete = models.IntegerField(blank=True, null=True)
    interval: Incomplete = models.IntegerField(blank=True, null=True)
    metric_group: Incomplete = models.IntegerField(blank=True, null=True)
    priority: Incomplete = models.IntegerField(blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True,
                                      null=True,
                                      default=lambda: int(time()))
    update_time: Incomplete = models.IntegerField(blank=True,
                                      null=True,
                                      default=lambda: int(time()))

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_circuit_configs'


class IastCircuitTarget(models.Model):
    circuit_config: Incomplete = models.ForeignKey(IastCircuitConfig,
                                       on_delete=models.CASCADE)
    target_type: Incomplete = models.IntegerField(blank=True, null=True)
    opt: Incomplete = models.IntegerField(blank=True, null=True)
    value: Incomplete = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_circuit_targets'


class IastCircuitMetric(models.Model):
    circuit_config: Incomplete = models.ForeignKey(IastCircuitConfig,
                                       on_delete=models.CASCADE)
    metric_type: Incomplete = models.IntegerField(blank=True, null=True)
    opt: Incomplete = models.IntegerField(blank=True, null=True)
    value: Incomplete = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_circuit_metrics'
