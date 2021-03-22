#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 11:04
# software: PyCharm
# project: sca

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from scaapi.views.artifacts import ArtifactView
from scaapi.views.search import SearchView
from scaapi.views.vul_count import VulCountView
from scaapi.views.vuls import VulsView

urlpatterns = [
    # ex: /api/search
    path('search', SearchView.as_view(), name='search'),
    path('artifacts', ArtifactView.as_view(), name='artifact'),
    path('vuls', VulsView.as_view(), name='vul'),
    path('vul/count', VulCountView.as_view(), name='vulcount'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
