#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/18 下午2:15
# software: PyCharm
# project: lingzhi-webapi
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group
from django.db import DatabaseError, transaction
from django.db.models import Q
from django.http import JsonResponse
from dongtai_models.models.errorlog import IastErrorlog
from dongtai_models.models.iast_vul_overpower import IastVulOverpower
from rest_framework.authtoken.models import Token

from base import R
from iast.base.user import TalentAdminEndPoint
from dongtai_models.models import User
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.asset import Asset
from dongtai_models.models.department import Department
from dongtai_models.models.heartbeat import Heartbeat
from dongtai_models.models.project import IastProject
from dongtai_models.models.strategy import IastStrategyModel
from dongtai_models.models.strategy_user import IastStrategyUser
from dongtai_models.models.system import IastSystem
from iast.serializers.user import UserSerializer


class UserEndPoint(TalentAdminEndPoint):
    @staticmethod
    def get_auth_departments(user, department_id=None):
        if user.is_system_admin():
            if department_id and int(department_id) != -1:
                departments = Department.objects.filter(id=department_id)
            else:
                departments = Department.objects.all()
        else:
            talent = user.get_talent()
            if department_id and int(department_id) != -1:
                departments = talent.departments.filter(id=department_id)
            else:
                departments = talent.departments.all()
        return departments

    @staticmethod
    def check_permission_with_talent(user, target_user):
        talent = user.get_talent()
        target_talent = target_user.get_talent()
        return user.is_system_admin() or talent == target_talent

    def get(self, request):
        """
        获取用户列表
        :param request:
        :return:
        """
        keywords = request.query_params.get('keywords')
        department_id = request.query_params.get('departmentId')

        departments = self.get_auth_departments(user=request.user, department_id=department_id)
        queryset = User.objects.filter(department__in=departments)
        if keywords:
            queryset = queryset.filter(
                Q(username__icontains=keywords) | Q(phone__icontains=keywords) | Q(email__icontains=keywords))

        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)

        try:
            page_summary, queryset = self.get_paginator(queryset, page, page_size)

            return JsonResponse({
                "status": 201,
                "msg": "success",
                "data": UserSerializer(queryset, many=True).data,
                "page": page_summary,
                "total": page_summary['alltotal']
            })
        except ValueError as e:
            return R.failure(msg='page和pageSize必须是数字')

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            talent = user.get_talent()
            if self.check_permission_with_talent(request.user, user):
                # 检查
                department = request.data.get('department')
                department_name = department.get('name', None)
                if department_name and department_name != user.department.get().get_department_name():
                    department = talent.departments.filter(name=department_name).first()
                    if department:
                        # todo 删除历史部门与用户的关系
                        user.department.set(department)

                role = int(request.data.get("role", 0))
                if role and role != user.is_superuser and role in [0, 2]:
                    user.is_superuser = role

                email = request.data.get('email')
                if email and email != user.email:
                    user.email = email

                phone = request.data.get('phone')
                if phone and phone != user.phone:
                    user.phone = phone

                password = request.data.get('password')
                if password and password != '':
                    user.set_password(password)

                user.save()

                return JsonResponse({
                    "status": 201,
                    "msg": "数据更新成功"
                })
            else:
                return JsonResponse({
                    "status": 203,
                    "msg": "no permission"
                })

        except DatabaseError as e:
            return JsonResponse({
                "status": 202,
                "msg": str(e)
            })

    def delete(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        username = user.get_full_name()
        if self.check_permission_with_talent(request.user, user):
            agents = IastAgent.objects.filter(user=user)
            if agents:
                IastErrorlog.objects.filter(agent__in=agents)
                Heartbeat.objects.filter(agent__in=agents)
                Asset.objects.filter(agent__in=agents)
                IastVulOverpower.objects.filter(agent__in=agents)

            try:
                IastSystem.objects.filter(user=user).delete()
                IastStrategyModel.objects.filter(user=user).delete()
                Token.objects.filter(user=user).delete()
                LogEntry.objects.filter(user=user).delete()
                IastStrategyUser.objects.filter(user=user).delete()
                IastProject.objects.filter(user=user).delete()
                department = user.department.get()
                department.users.remove(user)
                group = user.groups.get()
                group.user_set.remove(user)
                user.delete()
            except:
                return JsonResponse({
                    "status": 202,
                    "msg": f"用户{username}删除失败"
                })

        return JsonResponse({
            "status": 201,
            "msg": f"用户{username}删除成功"
        })

    @transaction.atomic
    def put(self, request):
        try:
            password = request.data.get('password')
            re_password = request.data.get('re_password')
            if password and re_password and password != '' and password == re_password:
                pass
            else:
                return JsonResponse({
                    "status": 204,
                    "msg": '密码一致'
                })

            username = request.data.get('username')
            if username:
                exist_user = User.objects.filter(username=username).count()
                if exist_user:
                    return JsonResponse({
                        "status": 205,
                        "msg": '用户名已存在'
                    })

            talent = request.user.get_talent()
            department = request.data.get('department')
            department_id = department.get('id')
            if department_id is None:
                return JsonResponse({
                    "status": 204,
                    "msg": '部门不存在'
                })

            _department = talent.departments.filter(id=department_id).first()
            if _department:
                email = request.data.get('email')
                role = request.data.get('role')
                phone = request.data.get('phone')

                if role == 0:
                    new_user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        phone=phone
                    )
                    _department.users.add(new_user)
                    group, success = Group.objects.get_or_create(name='user')
                    group.user_set.add(new_user)
                elif role == 2:
                    new_user = User.objects.create_talent_user(
                        username=username,
                        password=password,
                        email=email,
                        phone=phone
                    )
                    _department.users.add(new_user)
                    group, success = Group.objects.get_or_create(name='talent_admin')
                    group.user_set.add(new_user)
                else:
                    return JsonResponse({
                        "status": 202,
                        "msg": "用户创建失败"
                    })

                return JsonResponse({
                    "status": 201,
                    "msg": f"用户{username}创建成功"
                })
            else:
                return JsonResponse({
                    "status": 203,
                    "msg": "部门不存在或无访问权限"
                })
        except Exception as e:
            return JsonResponse({
                "status": 202,
                "msg": "用户创建失败"
            })
