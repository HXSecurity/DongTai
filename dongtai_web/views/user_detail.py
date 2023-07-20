#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi

from dongtai_common.endpoint import R
from dongtai_common.endpoint import TalentAdminEndPoint
from dongtai_common.models import User
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema


class UserDetailEndPoint(TalentAdminEndPoint):
    @extend_schema(
        summary=_("用户详情"),
        tags=[_("User")],
    )
    def get(self, request, user_id):
        try:
            user = User.objects.filter(id=user_id).first()
            talent = user.get_talent()

            if talent:
                current_talent = request.user.get_talent()
                if current_talent == talent:
                    department = user.get_department()
                    return R.success(
                        data={
                            "username": user.get_username(),
                            "department": department.get_department_name(),
                            "talent": talent.get_talent_name(),
                        }
                    )
        except BaseException:
            pass
        return R.failure(status=203, msg=_("no permission"))
