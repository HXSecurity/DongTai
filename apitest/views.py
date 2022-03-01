from django.shortcuts import render

from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.api_route import (
    IastApiRoute,
    IastApiMethod,
    HttpMethod,
    IastApiResponse,
    IastApiMethodHttpMethodRelation,
    IastApiParameter,
)
from iast.views.api_route_search import serialize
from django.db.models import Q
from apitest.utils import (
    swagger_trans,
    runtest,
)
from dongtai.models.project import IastProject
from dongtai.models.res_header import ProjectSaasMethodPoolHeader
from django.utils.translation import gettext_lazy as _
from iast.views.project_add import url_validate
from io import BytesIO
import json
from wsgiref.util import FileWrapper
from django.http import FileResponse


class ApiTestTriggerEndpoint(UserEndPoint):
    def get(self, request, pk):
        auth_users = self.get_auth_users(request.user)
        users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(
            user__in=users, pk=pk).order_by('-latest_time').first()
        if not project:
            return R.failure(msg=_('no project found'))
        if not project.base_url:
            return R.failure(msg=_(
                'Please enter the parameters required for the test first'))
        agents = IastAgent.objects.filter(user__in=auth_users,
                                          bind_project_id=pk).values("id")
        q = Q(agent__in=agents)
        if not IastApiRoute.objects.filter(q).exists():
            return R.failure(msg=_('No API collected'))
        api_routes = IastApiRoute.objects.filter(q).all()
        datas = [serialize(api_route) for api_route in api_routes]
        swaggerdatas = swagger_trans(datas)
        if project.test_req_header_key == '' or project.test_req_header_value == '':
            header_dict = {}
        else:
            header_dict = {
                project.test_req_header_key: project.test_req_header_value
            }
        runtest(swaggerdatas, header_dict, project.base_url)
        return R.success(msg=_('Starting API Test'))


class ApiTestOpenapiSpecEndpoint(UserEndPoint):
    def get(self, request, pk):
        auth_users = self.get_auth_users(request.user)
        users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(
            user__in=users, pk=pk).order_by('-latest_time').first()
        if not project:
            return R.failure(msg='no project found')
        agents = IastAgent.objects.filter(user__in=auth_users,
                                          bind_project_id=pk).values("id")
        q = Q(agent__in=agents)
        if not IastApiRoute.objects.filter(q).exists():
            return R.failure(msg=_('No API collected'))
        api_routes = IastApiRoute.objects.filter(q).all()
        datas = [serialize(api_route) for api_route in api_routes]
        swaggerdatas = swagger_trans(datas)
        swaggerfile = BytesIO()
        swaggerfile.write(json.dumps(swaggerdatas).encode())
        swaggerfile.seek(0)
        response =  FileResponse(
            FileWrapper(swaggerfile),
            filename=f'{project.name}-openapi.json',
        )
        response['Content-Type'] = 'application/json;charset=utf-8'
        return response


class ApiTestHeaderEndpoint(UserEndPoint):
    def get(self, request, pk):
        auth_users = self.get_auth_users(request.user)
        agents = IastAgent.objects.filter(user__in=auth_users,
                                          bind_project_id=pk).values("id")
        q = Q(agent__in=agents)
        headers = list(
            ProjectSaasMethodPoolHeader.objects.filter(q).values_list(
                'key', flat=True).distinct().all())
        return R.success(data=headers)
