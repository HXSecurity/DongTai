######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route_search
# @created     : Wednesday Aug 18, 2021 14:31:17 CST
#
# @description :
######################################################################

from django.db.models import Q
from dongtai.endpoint import R, UserEndPoint
from dongtai.models.api_route import IastApiRoute, IastApiMethod, IastApiRoute, HttpMethod, IastApiResponse, IastApiMethodHttpMethodRelation, IastApiParameter
from dongtai.models.agent import IastAgent
from iast.base.project_version import get_project_version, get_project_version_by_id
import hashlib
from dongtai.models.agent_method_pool import MethodPool
from django.forms.models import model_to_dict
from iast.utils import checkcover, batch_queryset


class ApiRouteSearch(UserEndPoint):
    def get(self, request):
        page_size = int(request.query_params.get('page_size', 1))
        page_index = int(request.query_params.get('page_index', 1))
        uri = request.query_params.get('uri', None)
        http_method = request.query_params.get('http_method', None)
        project_id = request.query_params.get('project_id', None)
        version_id = request.query_params.get('version_id', None)
        exclude_id = request.query_params.get('exclude_ids', None)
        exclude_id = [int(i)
                      for i in exclude_id.split(',')] if exclude_id else None
        is_cover = request.query_params.get('is_cover', None)
        is_cover_dict = {1: True, 0: False}
        is_cover = is_cover_dict[int(is_cover)] if is_cover else None
        auth_users = self.get_auth_users(request.user)

        if http_method:
            http_method_obj = HttpMethod.objects.filter(method=http_method.upper())[0:1]
            if http_method_obj:
                api_methods = IastApiMethod.objects.filter(
                    http_method__id=http_method_obj[0].id).all().values('id')
        else:
            api_methods = []

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
        q = q & Q(
            method_id__in=[_['id']
                           for _ in api_methods]) if api_methods != [] else q
        q = q & Q(path__icontains=uri) if uri else q
        q = q & ~Q(pk__in=exclude_id) if exclude_id else q
        api_routes = IastApiRoute.objects.filter(q).order_by('id').all()
        api_routes = _filter_and_label(
            api_routes, page_size, agents, http_method,
            is_cover) if is_cover else _filter_and_label(
                api_routes, page_size, agents, http_method)
        return R.success(
            data=[_serialize(api_route) for api_route in api_routes])


def _filter_and_label(api_routes, limit, agents, http_method, is_cover=None):
    api_routes_after_filter = []
    for api_route in batch_queryset(api_routes):
        api_route.is_cover = checkcover(api_route, agents, http_method)
        if is_cover is not None:
            api_routes_after_filter += [
                api_route
            ] if api_route.is_cover == is_cover else []
        else:
            api_routes_after_filter += [api_route]
        if limit == len(api_routes_after_filter):
            break
    return api_routes_after_filter




def _serialize(api_route):
    item = model_to_dict(api_route)
    item['is_cover'] = api_route.is_cover
    item['parameters'] = _get_parameters(api_route)
    item['responses'] = _get_responses(api_route)
    item['method'] = _get_api_method(item['method'])
    return item


def _get_parameters(api_route):
    parameters = IastApiParameter.objects.filter(route=api_route).all()
    return [model_to_dict(parameter) for parameter in parameters]


def _get_responses(api_route):
    #responses = api_route.IastApiResponse__set.all()
    responses = IastApiResponse.objects.filter(route=api_route).all()
    return [model_to_dict(response) for response in responses]


def _get_api_method(api_method_id):
    apimethod = IastApiMethod.objects.filter(pk=api_method_id).first()
    if apimethod:
        res = {}
        res['apimethod'] = apimethod.method
        res['httpmethods'] = [_.method for _ in apimethod.http_method.all()]
        return res
    return {}
