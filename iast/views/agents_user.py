#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from dongtai.endpoint import UserEndPoint, R
from dongtai.models.agent import IastAgent



class UserAgentList(UserEndPoint):
    def get(self, request):
        user = request.user
        if user.is_talent_admin():
            queryset = IastAgent.objects.all()
        else:
            queryset = IastAgent.objects.filter(user=user)
        queryset_datas = queryset.values("id", "token")
        data = []
        if queryset_datas:
            for item in queryset_datas:
                data.append({
                    "id": item['id'],
                    "name": item['token']
                })
        return R.success(data=data)
