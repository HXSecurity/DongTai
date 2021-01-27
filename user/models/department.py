#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午5:50
# software: PyCharm
# project: lingzhi-agent-server
import time

from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models.talent import Talent


class PermissionsMixin(models.Model):
    # manytomanyfield 通过 get/all/filter等方法转换为queryset
    talent = models.ManyToManyField(
        Talent,
        verbose_name=_('talent'),
        blank=True,
        help_text=_(
            'The talent this department belongs to. A department will get all permissions '
            'granted to each of their talent.'
        ),
        related_name="departments",
        related_query_name="department",
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

    class Meta:
        managed = False
        db_table = 'auth_department'

    def get_department_name(self):
        return self.name
