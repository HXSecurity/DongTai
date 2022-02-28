#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging

import time
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse
from dongtai.endpoint import SystemAdminEndPoint, R
from dongtai.models import User
from dongtai.models.department import Department
from dongtai.models.talent import Talent

from iast.serializers.talent import TalentSerializer
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('dongtai-webapi')


class TalentEndPoint(SystemAdminEndPoint):
    name = 'api-v1-talent'
    description = _('Tenant management')

    def get(self, request):
        """
        :param request:
        :return:
        """
        queryset = Talent.objects.all()

        name = request.query_params.get('name')
        if name:
            queryset = queryset.filter(talent_name__icontains=name)

        created = request.query_params.get('created')
        if created:
            users = User.objects.filter(username__icontains=created).values('id')
            ids = [_['id'] for _ in users] if users else []
            queryset = queryset.filter(created_by__in=ids)

        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 10))
        page_summary, proall = self.get_paginator(queryset, page, page_size)
        return JsonResponse({
            'status': 201,
            'msg': '',
            'data': TalentSerializer(queryset, many=True).data,
            "page": page_summary,
            "total": len(queryset)
        })

    def post(self, request, pk):
        """
        :param request:
        :param pk:
        :return:
        """
        talent = Talent.objects.filter(id=pk).first()
        if talent:
            talent.created_by = request.user.id
            talent.update_time = int(time.time())

            talent_name = request.data.get('talent_name')
            if talent_name:
                talent.talent_name = talent_name

            is_active = request.data.get('is_active')
            if is_active is not None:
                talent.is_active = bool(is_active)

            talent.save()

            return JsonResponse({
                'status': 201,
                'msg': 'success'
            })
        else:
            return JsonResponse({
                'status': 202,
                'msg': _('Tenant has been deactivated') if talent else _('Tenant does not exist')
            })

    def put(self, request):
        """
        :param request:
        :return:
        """
        talent_name = request.data.get('talent_name', None)
        talent_email = request.data.get('email', None)
        if talent_name is None or talent_email is None:
            return R.failure(msg=_('Tenant name or email is not specified'))
        status, msg = self.init_talent(talent_name, talent_email, request.user.id, request.user.get_username())
        if status:
            return R.success(msg=_(
                'Tenant {} has been created successfully').format(talent_name))
        return R.failure(msg=_('Tenant {} creation failed, error message:{}').
                         format(talent_name, msg))

    def delete(self, request, pk):
        """
        :param request:
        :return:
        """
        talent = Talent.objects.filter(id=pk).first()
        msg = _('Tenant: {} Delete successfully').format(talent.get_talent_name())
        departments = talent.departments.all()
        for department in departments:
            department.users.all().delete()
        departments.delete()
        talent.delete()
        return JsonResponse({
            'status': 201,
            'msg': msg,
        })

    @staticmethod
    @transaction.atomic
    def init_talent(talent_name, talent_email, created_by, default_username):
        try:
            logger.info(_('Query if the default tenant information exists'))
            suffix_email = talent_email.split('@')[-1]
            email = f'{default_username}@{suffix_email}'
            if User.objects.filter(username=email).exists():
                logger.error(_('Tenant information already exists, please delete tenant information first'))
                return False, _('The tenant information already existed, please delete the existing information first')

            logger.info(_('Started creating a tenant'))
            timestamp = int(time.time())
            talent = Talent(talent_name=talent_name, create_time=timestamp, update_time=timestamp,
                            created_by=created_by)
            talent.save()

            logger.info(_('Finished creating tenant, start to create tenant default department'))
            default_department = Department(name=_('Default department'), create_time=timestamp, update_time=timestamp,
                                            created_by=created_by)
            default_department.save()
            talent.departments.add(default_department)

            logger.info(_('Finished creating department, start to create default user'))

            password = '123456'
            default_user = User.objects.create_talent_user(username=email, password=password, email=email,
                                                           phone='11111111111')
            default_user.is_active = True
            default_user.save()

            group, success = Group.objects.get_or_create(name='talent_admin')
            group.user_set.add(default_user)
            group.save()

            default_department.users.add(default_user)
            logger.info(_('Finsihed creating and initializing tenant'))
            return True, 'success'
        except Exception as e:
            logger.error(_('Failed to created a tenant, error message:{}').format(e))
            return False, str(e)
