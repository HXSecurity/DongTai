#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi
from django.contrib.auth import authenticate

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from django.utils.translation import gettext_lazy as _


class UserPassword(UserEndPoint):
    name = "api-v1-user-password"
    description = _("change Password")

    def post(self, request):
        user = request.user
        
        if not request.data['old_password'] or not request.data['new_password']:
            return R.failure(msg=_('The password is not allowed to be empty'))
        else:
            user_check = authenticate(username=user.username, password=request.data['old_password'])
            if user_check is not None and user_check.is_active:
                password = request.data['new_password']
                
                user.set_password(password)
                user.save(update_fields=['password'])
                return R.success(msg=_('Password reset complete'))
            else:
                return R.failure(msg=_('Original password error'))
