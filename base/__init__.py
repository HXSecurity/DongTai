#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/21 下午8:40
# software: PyCharm
# project: lingzhi-webapi
from django.http import JsonResponse


class R:
    @staticmethod
    def success(data=None, msg="success", page=None, desc=None, total=None, token=None, upgrade_url=None,
                level_data=None, user_token=None, step=None):
        raw = {
            "status": 201,
            "msg": msg,
            "data": data
        }
        if page:
            raw['page'] = page
        if desc:
            raw['desc'] = desc
        if total:
            raw['total'] = total
        if token:
            raw['token'] = token
        if upgrade_url:
            raw['upgrade_url'] = upgrade_url
        if level_data:
            raw['level_data'] = level_data
        if user_token:
            raw['user_token'] = user_token
        if step:
            raw['step'] = step

        return JsonResponse(raw)

    @staticmethod
    def failure(data=None, msg="failure", status=None, desc=None):
        raw = {
            "status": 202,
            "msg": msg,
            "data": data
        }
        if desc:
            raw['desc'] = desc

        if status:
            return JsonResponse(raw, status=status)
        else:
            return JsonResponse(raw)
