#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午7:40
# software: PyCharm
# project: lingzhi-agent-server
import logging

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView

from account.models import User
from vuln.models.agent import IastAgent

logger = logging.getLogger('lingzhi.webapi')


class EndPoint(APIView):
    """
    基于APIView封装的API入口处理类，需要针对请求进行统一处理的都通过该类实现
    """
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
        """
        处理HTTP请求的入口方法
        :param request: HTTP请求
        :param args: 请求参数
        :param kwargs:
        :return: HTTP响应体
        """
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
            logger.error(f"HTTP请求处理出错，错误详情：{exc}")
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
        page_summary = {"alltotal": page_info.count, "num_pages": page_info.num_pages, "page_size": page_size}
        return page_summary, page_info.get_page(page).object_list if page != 0 else []

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

    def parse_args(self, request, func):
        try:
            return func(request)
        except Exception as e:
            logger.error(f"参数解析出错，错误原因：{e}")
            return None


class AnonymousAuthEndPoint(EndPoint):
    """
    具有匿名用户权限验证的API入口
    """
    authentication_classes = []


class SessionAuthEndPoint(EndPoint):
    """
    通过Session验证用户的API入口
    """
    authentication_classes = (SessionAuthentication,)


class TokenAuthEndPoint(EndPoint):
    """
    通过Token验证用户的API入口
    """
    authentication_classes = (TokenAuthentication,)


class MixinAuthEndPoint(EndPoint):
    """
    通过Token和Sessin验证的API入口
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)


class R:
    @staticmethod
    def success(status=201, data=None, msg="success", page=None, **kwargs):
        resp_data = {"status": status, "msg": msg}
        if data is not None:
            resp_data['data'] = data
        if page:
            resp_data['page'] = page

        for key, value in kwargs.items():
            resp_data[key] = value

        return JsonResponse(resp_data)

    @staticmethod
    def failure(data=None, msg="failure"):
        resp_data = {"status": 202, "msg": msg}
        if data:
            resp_data['data'] = data
        return JsonResponse(resp_data)
