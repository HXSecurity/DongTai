#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/25 下午6:43
# software: PyCharm
# project: dongtai-models

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai_common.models.department import Department
from dongtai_common.utils.settings import get_managed


class PermissionsMixin(models.Model):
    department = models.ManyToManyField(
        Department,
        verbose_name=_('department'),
        blank=True,
        help_text=_(
            'The department this user belongs to. A user will get all permissions '
            'granted to each of their department.'
        ),
        related_name="users",
        related_query_name="user",
    )

    class Meta:
        abstract = True


class SaaSUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', 0)
        return self._create_user(username, email, password, **extra_fields)

    def create_talent_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', 2)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') != 2:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def create_system_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') != 1:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    is_superuser = models.IntegerField(default=0)
    phone = models.CharField(max_length=15)
    default_language = models.CharField(max_length=15)
    objects = SaaSUserManager()

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def is_talent_admin(self):
        return self.is_superuser == 2 or self.is_superuser == 1

    def is_system_admin(self):
        return self.is_superuser == 1

    def get_talent(self):
        department = self.department.get() if self else None
        talent = department.talent.get() if department else None
        return talent

    def get_department(self):
        return self.department.get()
