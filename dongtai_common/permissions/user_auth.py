# 通过当前用户id,筛选出更高级管理员用户id
from dongtai_common.models.user import User


def super_of_cur_user(user_id):
    User.objects.filter(pk=user_id).first()

    return []
