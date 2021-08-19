######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route_search
# @created     : Wednesday Aug 18, 2021 14:31:17 CST
#
# @description :
######################################################################

from django.db.models import Q
from dongtai.endpoint import R, UserEndPoint
from dongtai.models.api_route import IastApiRoute, IastApiMethod, IastApiRoute, HttpMethod, IastApiResponse
from dongtai.models.agent import IastAgent
from iast.base.project_version import get_project_version, get_project_version_by_id
import hashlib
from dongtai.models.agent_method_pool import MethodPool
from django.forms.models import model_to_dict


class ApiRouteSearch(UserEndPoint):
    def get(self, request):
        page_size = int(request.query_params.get('page_size', 1))
        page = int(request.query_params.get('page_index', 1))
        uri = request.query_params.get('uri', None)
        http_method = request.query_params.get('http_method', None)
        project_id = request.query_params.get('project_id', None)
        version_id = request.query_params.get('version_id', None)
        auth_users = self.get_auth_users(request.user)

        api_methods = IastApiMethod.objects.filter(
            http_method__method=http_method).all().values('id')

        if not version_id:
            current_project_version = get_project_version(
                project_id, auth_users)
        else:
            current_project_version = get_project_version_by_id(version_id)
        agents = IastAgent.objects.filter(
            user__in=auth_users,
            bind_project_id=project_id,
            project_version_id=current_project_version.get("version_id",
                                                           0)).values("id")
        q = Q(agent_id__in=[_['id'] for _ in agents])
        q = q & Q(method_id__in=[_['method_id'] for _ in api_methods])
        q = q & Q(uri__icontains=uri)
        api_routes = IastApiRoute.objects.filter(q).all()
        summary, api_routes = self.get_paginator(api_routes, page, page_size)
        return R.success(
            data=[_serialize(api_route) for api_route in api_routes],
            page=summary)


def _serialize(api_route):
    item = model_to_dict(api_route)
    item['is_cover'] = _checkcover(api_route, agents)
    item['parameters'] = _get_parameters(api_routes)
    return item


def _get_parameters(api_route):
    parameters = api_route.IastApiParameter__set.all()
    return [model_to_dict(parameter) for parameter in parameters]


def _get_responses(api_route):
    responses = api_route.IastApiResponse__set.all()
    return [model_to_dict(response) for response in responses]


def _checkcover(api_route, agents, http_method):
    uri_hash = hashlib.sha1(api_route.url.encode('utf-8')).hexdigest()
    api_method_id = api_route.values('method_id')
    http_method_ids = IastApiMethodHttpMethodRelation.objects.filter(
        api_method_id=api_method_id).values('api_method_id')
    http_methods = HttpMethod.objects.filter(
        http_method_ids__in=http_method_ids).all().values_list('method')
    q = Q(agent_id__in=[_['id'] for _ in agents])
    q = q & Q(http_method__in=http_methods)
    q = q & Q(uri_hash=uri_hash)
    if MethodPool.objects.filter(q).first():
        return True
    return False
