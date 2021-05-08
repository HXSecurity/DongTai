#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/24 下午9:07
# software: PyCharm
# project: lingzhi-webapi
from django.contrib.auth import authenticate

from base import R
from iast.base.user import UserEndPoint


class UserPassword(UserEndPoint):
    name = "api-v1-user-password"
    description = "修改密码"

    def post(self, request):
        user = request.user
        # edit by song 校验旧密码
        if not request.data['old_password'] or not request.data['new_password']:
            return R.failure(msg='密码不允许为空')
        else:
            user_check = authenticate(username=user.username, password=request.data['old_password'])
            if user_check is not None and user_check.is_active:
                password = request.data['new_password']
                # todo 增加用户密码格式验证
                user.set_password(password)
                user.save(update_fields=['password'])
                return R.success(msg='密码修改成功')
            else:
                return R.failure(msg='原始密码错误')
