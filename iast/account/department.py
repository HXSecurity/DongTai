#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/18 下午2:16
# software: PyCharm
# project: lingzhi-webapi
import queue
import time

from django.db import transaction
from django.http import JsonResponse

from iast.base.user import TalentAdminEndPoint
from dongtai_models.models.department import Department
from dongtai_models.models.talent import Talent


class DepartmentEndPoint(TalentAdminEndPoint):

    @staticmethod
    def get_department_tree(talent_name, queryset):
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

        return department_tree

    def get(self, request):
        """
        部门列表，支持查询条件
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
            data.append(self.get_department_tree(talent_name=talent_name, queryset=queryset))

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
        更新部门信息
        :param request:
        :param pk: 部门ID
        :return:
        """
        user = request.user

        department = self.has_department_permission(user, pk)
        if department:
            name = request.data.get('name')
            if self.exist(name):
                return JsonResponse({
                    'status': 202,
                    'msg': f'部门{name}已存在'
                })
            else:
                department.created_by = request.user.id
                department.update_time = int(time.time())
                department.name = name
                department.save()

                return JsonResponse({
                    'status': 201,
                    'msg': f'部门名称已修改为{name}'
                })
        else:
            return JsonResponse({
                'status': 202,
                'msg': '部门不存在'
            })

    @staticmethod
    def has_department_permission(user, department_id):
        if user.is_system_admin():
            parent_exist = Department.objects.filter(id=department_id).first()
        else:
            talent = user.get_talent()
            parent_exist = talent.departments.filter(id=department_id).first()
        return parent_exist

    @transaction.atomic
    def put(self, request):
        """
        创建部门
        :param request:
        :return:
        """
        name = request.data.get('name')
        parent = request.data.get('parent')
        if name and parent and int(parent) != 0:
            if self.exist(name):
                return JsonResponse({
                    'status': 202,
                    'msg': f'部门{name}已存在'
                })
            else:
                # 检查父部门是否为当前租户
                if parent == -1 or self.has_department_permission(request.user, parent):
                    timestamp = int(time.time())
                    department = Department(name=name, create_time=timestamp, update_time=timestamp,
                                            created_by=request.user.id, parent_id=int(parent))
                    department.save()
                    talent = request.user.get_talent()
                    talent.departments.add(department)
                    return JsonResponse({
                        'status': 201,
                        'msg': f'部门{name}创建成功',
                        'data': department.id
                    })
                else:
                    return JsonResponse({
                        'status': 203,
                        'msg': '父部门无访问权限'
                    })
        else:
            return JsonResponse({
                'status': 202,
                'msg': '部门不存在'
            })

    @transaction.atomic
    def delete(self, request, pk):
        department = self.has_department_permission(request.user, pk)
        user_count = department.users.count()
        force = bool(request.data.get('force', 'false'))
        if user_count > 0:
            if force:
                department.users.delete()
                department.delete()
            else:
                return JsonResponse({
                    'status': 202,
                    'msg': f'删除失败，部门{department.get_department_name()}下存在用户，请执行强制删除',
                })
                pass
        else:
            department.delete()
        return JsonResponse({
            'status': 201,
            'msg': '删除成功'
        })
