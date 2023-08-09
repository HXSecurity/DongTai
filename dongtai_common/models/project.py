#!/usr/bin/env python
# datetime:2020/11/30 下午5:32
import time

from django.db import models

from dongtai_common.models import User
from dongtai_common.models.department import Department
from dongtai_common.models.strategy_user import IastStrategyUser
from dongtai_common.utils.db import get_timestamp
from dongtai_common.utils.settings import get_managed


class VulValidation(models.IntegerChoices):
    FOLLOW_GLOBAL = 0
    ENABLE = 1
    DISABLE = 2
    __empty__ = 0


class ProjectStatus(models.IntegerChoices):
    NORMAL = 0, "正常"
    ERROR = 1, "错误"
    OFFLINE = 2, "离线"
    __empty__ = 0


class IastProjectTemplate(models.Model):
    template_name = models.CharField(max_length=255)
    latest_time = models.IntegerField(default=get_timestamp)
    user = models.ForeignKey(User, models.DO_NOTHING)
    scan = models.ForeignKey(IastStrategyUser, models.DO_NOTHING)
    vul_validation = models.IntegerField(default=0, choices=VulValidation.choices)
    is_system = models.IntegerField(default=0)
    data_gather = models.JSONField(default=dict)
    data_gather_is_followglobal = models.IntegerField(default=1)
    blacklist_is_followglobal = models.IntegerField(default=1)

    class Meta:
        managed = get_managed()
        db_table = "iast_project_template"

    def to_full_template(self):
        pass

    def to_full_project_args(self):
        return {
            "scan_id": self.scan_id,  # type: ignore
            "vul_validation": self.vul_validation,
            "data_gather": self.data_gather,
            "data_gather_is_followglobal": self.data_gather_is_followglobal,
            "blacklist_is_followglobal": self.blacklist_is_followglobal,
        }


class IastProject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    mode = models.CharField(default="插桩模式", max_length=255, blank=True)
    vul_count = models.PositiveIntegerField(blank=True, null=True)
    agent_count = models.IntegerField(blank=True, null=True)
    latest_time = models.IntegerField(default=get_timestamp)
    user = models.ForeignKey(User, models.DO_NOTHING)
    # openapi服务不必使用该字段
    scan = models.ForeignKey(IastStrategyUser, models.DO_NOTHING, blank=True, null=True)

    vul_validation = models.IntegerField(default=0, choices=VulValidation.choices)
    base_url = models.CharField(max_length=255, blank=True)
    test_req_header_key = models.CharField(max_length=511, blank=True)
    test_req_header_value = models.CharField(max_length=511, blank=True)
    data_gather = models.JSONField(null=True)
    data_gather_is_followglobal = models.IntegerField(default=1)
    blacklist_is_followglobal = models.IntegerField(default=1)
    department = models.ForeignKey(Department, models.DO_NOTHING)
    template = models.ForeignKey(IastProjectTemplate, models.DO_NOTHING)
    enable_log = models.BooleanField(null=True)
    log_level = models.CharField(max_length=511, null=True, blank=True)
    last_has_online_agent_time = models.IntegerField(default=get_timestamp)
    status = models.IntegerField(default=0, choices=ProjectStatus.choices)
    projectgroups = models.ManyToManyField("IastProjectGroup", through="IastProjectGroupProject")
    users = models.ManyToManyField("User", through="IastProjectUser", related_name="auth_projects")

    class Meta:
        managed = get_managed()
        db_table = "iast_project"

    def update_latest(self):
        self.latest_time = int(time.time())
        self.save(update_fields=["latest_time"])


class IastProjectUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_constraint=False)
    project = models.ForeignKey(IastProject, models.DO_NOTHING, db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = "iast_project_user"
        constraints = [
            models.UniqueConstraint(fields=["project_id", "user_id"], name="iast_project_user_unique_constraint")
        ]
        indexes = [models.Index(fields=["user_id", "project_id"])]
