#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 上午10:04
# software: PyCharm
# project: sentry
import json

from django.contrib.admin.models import LogEntryManager, CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from dongtai_models.models import User
from dongtai_models.models.agent import IastAgent
from rest_framework import status, exceptions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_proxy.views import ProxyView


class EndPoint(APIView):
    name = "api-v1"
    description = "API接口"

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        super().__init__(**kwargs)
        self.log_manager = LogEntryManager()
        self.log_manager.model = LogEntry

    def load_json_body(self, request):
        """
        Attempts to load the request body when it's JSON.

        The end result is ``request.json_body`` having a value. When it can't
        load the body as JSON, for any reason, ``request.json_body`` is None.

        The request flow is unaffected and no exceptions are ever raised.
        """

        request.json_body = None

        if not request.META.get("CONTENT_TYPE", "").startswith("application/json"):
            return

        if not len(request.body):
            return

        try:
            request.json_body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return

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
        if self.request.user is not None and self.request.user.is_active:
            self.log_manager.log_action(
                user_id=self.request.user.id,
                content_type_id=ContentType.objects.get_or_create(app_label=self.request.content_type)[0].id,
                object_id='',
                object_repr='',
                action_flag=CHANGE,
                change_message=f'访问{self.description}接口'
            )
        return self.response

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, exceptions.Throttled):
            exc.status_code = status.HTTP_429_TOO_MANY_REQUESTS
        elif isinstance(exc, (exceptions.NotAuthenticated,
                              exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        return response

    def parse_args(self, request):
        pass

    @staticmethod
    def get_paginator(queryset, page=1, page_size=20):
        """
        根据模型集合、页号、每页大小获取分页数据
        :param queryset:
        :param page:
        :param page_size:
        :return:
        """
        if int(page_size) > 50:
            page_size = 50
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


class AnonymousAuthEndPoint(EndPoint):
    authentication_classes = []


class SessionAuthEndPoint(EndPoint):
    authentication_classes = (SessionAuthentication,)


class TokenAuthEndPoint(EndPoint):
    authentication_classes = (TokenAuthentication,)


class MixinAuthEndPoint(EndPoint):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)


class SessionAuthProxyView(ProxyView):
    authentication_classes = (SessionAuthentication,)

    def get_default_headers(self, request):
        headers = super().get_default_headers(request)
        if request.user.is_active:
            token, success = Token.objects.get_or_create(user=request.user)
            if token:
                headers['Authorization'] = f'Token {token.key}'
        return headers


class MixinAuthPoxyView(SessionAuthProxyView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)


class AnonymousAuthProxyView(ProxyView):
    authentication_classes = (SessionAuthentication,)
