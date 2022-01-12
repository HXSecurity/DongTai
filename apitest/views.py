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
# Create your views here.


class ApiTestTriggerEndpoint(UserEndPoint):
    def get(self, request, pk):
        auth_users = self.get_auth_users(request.user)
        users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(user__in=users,
                                             pk=pk).order_by('-latest_time').first()
        if not project:
            return R.failure(msg='no project found')
        if (project.test_req_header_key == ''
                or project.test_req_header_value == ''
                or project.base_url == ''):
            return R.failure(
                msg='Please enter the parameters required for the test first')
        agents = IastAgent.objects.filter(user__in=auth_users,
                                          bind_project_id=pk).values("id")
        q = Q(agent__in=agents)
        api_routes = IastApiRoute.objects.filter(q).all()
        datas = [serialize(api_route) for api_route in api_routes]
        swaggerdatas = swagger_trans(datas)
        runtest(swaggerdatas,
                {project.test_req_header_key: project.test_req_header_value},
                project.base_url)
        return R.success()


class ApiTestHeaderEndpoint(UserEndPoint):
    def get(self, request, pk):
        auth_users = self.get_auth_users(request.user)
        agents = IastAgent.objects.filter(user__in=auth_users,
                                          bind_project_id=pk).values("id")
        q = Q(agent__in=agents)
        headers = ProjectSaasMethodPoolHeader.objects.filter(q).values_list(
            'key').distinct().all()
        return R.success(data=headers)
