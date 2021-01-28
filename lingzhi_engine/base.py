#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午7:40
# software: PyCharm
# project: lingzhi-agent-server
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView

from account.models import User
from vuln.models.agent import IastAgent


class EndPoint(APIView):
    name = "api-v1"
    description = "ApiServer接口"

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        super().__init__(**kwargs)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    @staticmethod
    def get_paginator(queryset, page=1, page_size=20):
        """
        根据模型集合、页号、每页大小获取分页数据
        :param queryset:
        :param page:
        :param page_size:
        :return:
        """
        page_info = Paginator(queryset, per_page=page_size)
        if page <= 0 or page > page_info.num_pages:
            page = 0
        page_summary = {"alltotal": page_info.count, "num_pages": page_info.num_pages, "page_size": page_size}

        return page_summary, page_info.page(page).object_list if page != 0 else []

    @staticmethod
    def get_auth_users(user):
        """
        通过用户查询有访问权限的用户列表
        :param user:
        :return:
        """
        if user.is_system_admin():
            users = User.objects.all()
        elif user.is_talent_admin():
            talent = user.get_talent()
            departments = talent.departments.all()
            users = User.objects.filter(department__in=departments)
        else:
            users = [user]
        return users

    @staticmethod
    def get_auth_agents_with_user(user):
        """
        通过用户查询有访问权限的agent列表
        :param user:
        :return:
        """
        return EndPoint.get_auth_agents(EndPoint.get_auth_users(user))

    @staticmethod
    def get_auth_agents(users):
        """
        通过用户列表查询有访问权限的agent列表
        :param users:
        :return:
        """
        return IastAgent.objects.filter(user__in=users)


class AnonymousAuthEndPoint(EndPoint):
    authentication_classes = []


class SessionAuthEndPoint(EndPoint):
    authentication_classes = (SessionAuthentication,)


class TokenAuthEndPoint(EndPoint):
    authentication_classes = (TokenAuthentication,)


class MixinAuthEndPoint(EndPoint):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)


class R:
    @staticmethod
    def success(data=None, msg="success", page=None):
        return JsonResponse({
            "status": 201,
            "msg": msg,
            "data": data,
            "page": page
        })

    @staticmethod
    def failure(data=None, msg="failure"):
        return JsonResponse({
            "status": 202,
            "msg": msg,
            "data": data
        })
