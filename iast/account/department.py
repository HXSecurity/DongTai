#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import queue
import time

from django.db import transaction
from django.http import JsonResponse
from dongtai.endpoint import TalentAdminEndPoint

from dongtai.models.department import Department
from dongtai.models.talent import Talent
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from iast.utils import extend_schema_with_envcheck, get_response_serializer


class DepartmentPutArgSer(serializers.Serializer):
    name = serializers.CharField()
    parent = serializers.IntegerField()
    principal_id = serializers.IntegerField(required=False, default=0)


class DepartmentEndPoint(TalentAdminEndPoint):
    @staticmethod
    def get_department_tree(talent_id, talent_name, queryset):
        queryset = queryset.values('id', 'name', 'parent_id')

        department_tree = {
            'id': -1,
            'label': talent_name,
            'children': []
        }

        for raw_department in queryset:
            parent_id = raw_department['parent_id']
            q = queue.Queue()
            q.put(department_tree)

            found = False
            while found is False and q.empty() is False:
                data = q.get()
                if data['id'] == parent_id:
                    data['children'].append({
                        'id': raw_department['id'],
                        'label': raw_department['name'],
                        'children': [],
                    })
                    break
                else:
                    for children in data['children']:
                        q.put(children)
        department_tree['id'] = -talent_id
        return department_tree

    @extend_schema_with_envcheck(request=DepartmentPutArgSer,
                                 summary=_('部门'),
                                 description=_("部门获取"),
                                 tags=[_('管理')])
    def get(self, request):
        """
        :param request:
        :return:
        """
        current_user = request.user
        if current_user.is_system_admin():
            talents = Talent.objects.all()
        else:
            talents = [request.user.get_talent()]

        name = request.query_params.get('name')
        data = list()
        for talent in talents:
            talent_name = talent.get_talent_name()
            queryset = talent.departments.all()
            if name:
                queryset = queryset.filter(name__icontains=name)
            data.append(self.get_department_tree(talent_id=talent.id, talent_name=talent_name, queryset=queryset))

        return JsonResponse({
            'status': 201,
            'msg': '',
            'data': data,
        })

    @staticmethod
    def exist(name):
        department = Department.objects.filter(name=name).first()
        return True if department else False

    def post(self, request, pk):
        """
        :param request:
        :param pk: 
        :return:
        """
        user = request.user

        department = self.has_department_permission(user, pk)
        if department:
            name = request.data.get('name')
            if self.exist(name):
                return JsonResponse({
                    'status': 202,
                    'msg': _('Department {} already exists').format(name)
                })
            else:
                department.created_by = request.user.id
                department.update_time = int(time.time())
                department.name = name
                department.save()

                return JsonResponse({
                    'status': 201,
                    'msg': _('Department name has been modified to {}').format(name)
                })
        else:
            return JsonResponse({
                'status': 202,
                'msg': _('Department does not exist')
            })

    @staticmethod
    def has_department_permission(user, department_id):
        if user.is_system_admin():
            parent_exist = Department.objects.filter(id=department_id).first()
        else:
            talent = user.get_talent()
            parent_exist = talent.departments.filter(id=department_id).first()
        return parent_exist

    @extend_schema_with_envcheck(request=DepartmentPutArgSer,
                                 summary=_('部门'),
                                 description=_("增加部门"),
                                 tags=[_('管理')])
    @transaction.atomic
    def put(self, request):
        """
        :param request:
        :return:
        """
        name = request.data.get('name')
        parent = request.data.get('parent')
        talent = request.data.get('talent', None)
        if name and parent and int(parent) != 0:
            if self.exist(name):
                return JsonResponse({
                    'status': 202,
                    'msg': _('Department {} already exists').format(name)
                })
            else:
                if parent == -1 or self.has_department_permission(request.user, parent):
                    timestamp = int(time.time())
                    department = Department(name=name,
                                            create_time=timestamp,
                                            update_time=timestamp,
                                            created_by=request.user.id,
                                            parent_id=int(parent))
                    department.save()
                    talent_ = Talent.objects.filter(pk=talent).first()
                    if talent_ is None:
                        return JsonResponse({
                            'status': 202,
                            'msg': _('Talent does not exist')
                        })
                    talent = talent_ if talent and talent_ else request.user.get_talent(
                    )
                    talent.departments.add(department)
                    return JsonResponse({
                        'status': 201,
                        'msg': _('Department {} has been created successfully').format(name),
                        'data': department.id
                    })
                else:
                    return JsonResponse({
                        'status': 203,
                        'msg': _('Access Denied')
                    })
        else:
            return JsonResponse({
                'status': 202,
                'msg': _('Department does not exist')
            })

    @transaction.atomic
    def delete(self, request, pk):
        department = self.has_department_permission(request.user, pk)
        user_count = department.users.count()
        force = bool(request.query_params.get('force', ''))
        if user_count > 0:
            if force:
                department.users.delete()
                department.delete()
            else:
                return JsonResponse({
                    'status': 202,
                    'msg': _('Delete failed, existence of users under department {}, please implement forced deletion').format(department.get_department_name()),
                })
                pass
        else:
            department.delete()
        return JsonResponse({
            'status': 201,
            'msg': _('Deleted Successfully')
        })
