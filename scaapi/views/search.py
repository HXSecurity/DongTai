# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 14:05
# software: PyCharm
# project: sca

from rest_framework.response import Response

from base.endpoint import AnonymousAuthEndPoint
from iast.base.user import UserEndPoint


class SearchView(AnonymousAuthEndPoint):

    def get(self, request):
        """
        Return a list of all users.
        """

        return Response({"message": "Will not appear in schema!"})
