#!/usr/bin/env python
# datetime:2020/11/27 下午4:31
import time
from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai_common.models.talent import Talent
from dongtai_common.utils.customfields import trans_char_field
from dongtai_common.utils.settings import get_managed


class IastDepartment(models.Model):
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_department"


class PermissionsMixin(models.Model):
    talent = models.ManyToManyField(
        Talent,
        verbose_name=_("talent"),
        blank=True,
        help_text=_(
            "The talent this department belongs to. A department will get all permissions "
            "granted to each of their talent."
        ),
        related_name="departments",
        related_query_name="talent",
    )

    class Meta:
        abstract = True


class Department(PermissionsMixin):
    name = models.CharField(
        _("name"),
        unique=True,
        blank=True,
        max_length=100,
        error_messages={
            "unique": _("A department with that department name already exists."),
        },
    )
    create_time = models.IntegerField(
        _("create time"), default=lambda: int(time.time()), blank=True
    )
    update_time = models.IntegerField(
        _("update time"), default=lambda: int(time.time()), blank=True
    )
    created_by = models.IntegerField(_("created by"), blank=True)
    parent_id = models.IntegerField(_("parent id"), blank=True)
    principal_id = models.IntegerField(default=0, blank=True)
    department_path = models.CharField(max_length=1024, blank=True)
    token = models.CharField(max_length=1024, blank=True)

    class Meta:
        managed = get_managed()
        db_table = "auth_department"

    def get_department_name(self):
        return self.name

    @trans_char_field(
        "name", {"zh": {"默认部门": "默认部门"}, "en": {"默认部门": "default department"}}
    )
    def __getattribute__(self, name) -> Any:
        return super().__getattribute__(name)
