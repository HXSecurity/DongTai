######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route_related_request
# @created     : Saturday Aug 21, 2021 13:54:14 CST
#
# @description :
######################################################################

from dongtai_common.models.api_route import IastApiRoute
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_web.base.project_version import get_project_version, get_project_version_by_id
from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from dongtai_web.utils import sha1
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers


class ApiRouteCoverRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodPool
        fields = serializers.ALL_FIELDS


_GetResponseSerializer = get_response_serializer(ApiRouteCoverRelationSerializer())


class ApiRouteRelationRequest(UserEndPoint):
    @extend_schema_with_envcheck(
        [{
            'name': 'api_route_id',
            'type': int
        }, {
            'name': 'project_id',
            'type': int
        }, {
            'name': 'version_id',
            'type': int
        }],
        tags=[_('API Route')],
        summary=_('API Route Relation Request'),
        description=_("Get the coverrate of the project corresponding to the specified id."
                      ),
        response_schema=_GetResponseSerializer,
    )
    def get(self, request):
        try:
            page_size = int(request.query_params.get('page_size', 1))
            page_index = int(request.query_params.get('page_index', 1))
            api_route_id = int(request.query_params.get('api_route_id', 1))
            api_route = IastApiRoute.objects.filter(pk=api_route_id).first()
            if api_route is None:
                return R.failure(msg=_("API not Fould"))
            project_id = int(request.query_params.get('project_id', None))
            auth_users = self.get_auth_users(request.user)
            version_id = int(request.query_params.get('version_id', None))
        except BaseException:
            return R.failure(_("Parameter error"))
        if project_id:
            if not version_id:
                current_project_version = get_project_version(
                    project_id)
            else:
                current_project_version = get_project_version_by_id(version_id)
            agents = IastAgent.objects.filter(
                user__in=auth_users,
                bind_project_id=project_id,
                project_version_id=current_project_version.get(
                    "version_id", 0)).values("id")
        q = Q()
        q = q & Q(agent_id__in=[_['id'] for _ in agents]) if project_id else q
        q = q & Q(uri_sha1=sha1(api_route.path))
        q = q & Q(
            http_method__in=[_.method for _ in api_route.method.http_method.all()])
        method = MethodPool.objects.filter(q).order_by('-update_time')[0:1].values()
        if method:
            return R.success(data=list(method)[0])
        else:
            return R.success(data={})
