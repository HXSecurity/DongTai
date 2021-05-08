#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/18 下午3:39
# software: PyCharm
# project: lingzhi-webapi

from base import R
from iast.base.user import TalentAdminEndPoint
from dongtai_models.models import User


class UserDetailEndPoint(TalentAdminEndPoint):
    def get(self, request, user_id):
        try:
            user = User.objects.filter(id=user_id).first()
            talent = user.get_talent()

            if talent:
                current_talent = request.user.get_talent()
                if current_talent == talent:
                    # 返回基本信息
                    department = user.get_department()
                    return R.success(data={
                        'username': user.get_username(),
                        'department': department.get_department_name(),
                        'talent': talent.get_talent_name()
                    })
        except:
            pass
        return R.failure(status=203, msg='no permission')
