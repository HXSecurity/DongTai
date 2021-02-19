#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/28 上午10:12
# software: PyCharm
# project: lingzhi-engine
from account.models import User
from lingzhi_engine import const
from lingzhi_engine.base import R
from vuln.base.method_pool import AnonymousAndUserEndPoint
from vuln.models.agent_method_pool import MethodPool
from vuln.serializers.method_pool import MethodPoolSerialize


class MethodPoolDetailEndPoint(AnonymousAndUserEndPoint):

    def get(self, request):
        try:
            method_pool_id = request.query_params.get('id')

            if method_pool_id:
                if request.user.is_active:
                    method_pool = MethodPool.objects.filter(agent__in=self.get_auth_agents_with_user(request.user),
                                                            id=method_pool_id).first()
                else:
                    # fixme 使用更加优雅的方法，开放靶场的agent数据给每一个用户
                    dt_range_user = User.objects.filter(username=const.USER_BUGENV).first()
                    if dt_range_user:
                        method_pool = MethodPool.objects.filter(agent__in=self.get_auth_agents_with_user(dt_range_user),
                                                                id=method_pool_id).first()
                    else:
                        R.failure(msg='no permission')
                # todo 方法池数据转换为调用链
                return R.success(data=MethodPoolSerialize(method_pool).data)
            return R.failure(msg='方法池ID为空')
        except ValueError as e:
            return R.failure(msg='page和pageSize只能为数字')
