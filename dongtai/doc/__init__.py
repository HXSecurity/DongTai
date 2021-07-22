#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/22 下午12:37
# project: dongtai-engine
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def schema_view(title, version, description, public=False):
    return get_schema_view(
        openapi.Info(
            title=title,
            default_version=version,
            description=description,
            terms_of_service="https://hxsecurity.github.io/DongTaiDoc/#/",
            contact=openapi.Contact(email="dongzhiyong@huoxian.cn"),
            license=openapi.License(name="BSD License"),
        ),
        validators=['ssv', 'flex'],
        public=public,
        permission_classes=(permissions.AllowAny,),
    )
