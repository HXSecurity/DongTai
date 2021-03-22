#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/4 下午3:50
# software: PyCharm
# project: lingzhi-webapi
from base import R
from iast.base.user import UserEndPoint
from webapi.settings import config


class OpenApiEndpoint(UserEndPoint):
    def get(self, request):
        return R.success(data={'url': config.get('apiserver', 'url')})
