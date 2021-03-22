#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 15:58
# software: PyCharm
# project: sca

from rest_framework import pagination


# 基础分页
class SCAPageNumberPagination(pagination.PageNumberPagination):
    # 默认一页显示的条数
    page_size = 10
    # 查询页面的关键字
    page_query_param = 'page'
    # 用户自定义一页显示条数的关键字
    page_size_query_param = 'page_size'
    # 用户最大可自定义一页显示的条数
    max_page_size = 20
