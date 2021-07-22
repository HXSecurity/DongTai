#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 下午4:31
# software: PyCharm
# project: dongtai-models
import time

from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai.models.talent import Talent


class IastDepartment(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_department'


class PermissionsMixin(models.Model):
    talent = models.ManyToManyField(
        Talent,
        verbose_name=_('talent'),
        blank=True,
        help_text=_(
            'The talent this department belongs to. A department will get all permissions '
            'granted to each of their talent.'
        ),
        related_name="departments",
        related_query_name="talent",
    )

    class Meta:
        abstract = True


class Department(PermissionsMixin):
    name = models.CharField(
        _('name'),
        unique=True,
        max_length=100,
        error_messages={
            'unique': _("A department with that department name already exists."),
        },
    )
    create_time = models.IntegerField(_('create time'), default=int(time.time()), blank=True)
    update_time = models.IntegerField(_('update time'), default=int(time.time()), blank=True)
    created_by = models.IntegerField(_('created by'), blank=True)
    parent_id = models.IntegerField(_('parent id'), blank=True)

    class Meta:
        managed = False
        db_table = 'auth_department'

    def get_department_name(self):
        return self.name
