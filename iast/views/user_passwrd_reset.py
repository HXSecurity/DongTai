#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/24 下午9:07
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai_models.models import User

from base import R
from iast.base.user import TalentAdminEndPoint

logger = logging.getLogger("dongtai-webapi")


class UserPasswordReset(TalentAdminEndPoint):
    name = "api-v1-user-password-reset"
    description = "重置密码"

    def post(self, request):
        try:
            user_id = request.data.get('userId')
            if user_id:
                user = User.objects.filter(id=user_id).first()
                if user:
                    username = user.get_username()
                    user.set_password(f'{username}@123')
                    user.save(update_fields=['password'])
                    msg = f'用户{username}密码重置成功'
                    return R.success(msg=msg)
                else:
                    msg = '用户不存在'
                    logger.warning(msg)
                    return R.failure(msg=msg)
            else:
                msg = 'userId为空'
                logger.error('用户ID为空')
                return R.failure(msg=msg)
        except ValueError as e:
            msg = 'userId必须为数字'
            logger.error(msg)
        except Exception as e:
            msg = f'密码重置失败，原因：{e}'
            logger.error(msg)
        return R.failure(msg=msg)
