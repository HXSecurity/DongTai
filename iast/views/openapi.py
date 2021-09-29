from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from webapi.settings import config
from dongtai.models.profile import IastProfile
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from urllib.parse import urlparse
from rest_framework import serializers

_PostResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('Created success')), ''),
    ((202, _('Current users have no permission to modify')), ''),
    ((202, _('Parameter error')), ''),
))


class OpenApiEndpointSerializer(serializers.Serializer):
    value = serializers.CharField(help_text='The openapi url')


class OpenApiEndpointGetResponseSerializer(serializers.Serializer):
    url = serializers.CharField(help_text='The openapi url')


_GetResponseSerializer = get_response_serializer(
    data_serializer=OpenApiEndpointGetResponseSerializer(),
    status_msg_keypair=(
        ((201, _('success')), ''),
        ((202, _('Get OpenAPI configuration failed')), ''),
    ))


class OpenApiEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_('Profile')],
        summary=_('Profile DongTai-OpenApi Retrieve'),
        description=_("Get the uri of DongTai-OpenApi"),
        response_schema=_GetResponseSerializer,
    )
    def get(self, request):
        profilefromdb = IastProfile.objects.filter(
            key='apiserver').values_list('value', flat=True).first()
        profilefromini = None
        profiles = list(
            filter(lambda x: x is not None, [profilefromdb, profilefromini]))
        if profiles == [] or not profiles[0]:
            return R.failure(msg=_("Get OpenAPI configuration failed"))
        return R.success(data={'url': profiles[0]})

    @extend_schema_with_envcheck(
        request=OpenApiEndpointSerializer,
        tags=[_('Profile')],
        summary=_('Profile DongTai-OpenApi Modify'),
        description=
        _("To set the url address of DongTai-OpenApi, administrator rights are required"
          ),
        response_schema=_PostResponseSerializer,
    )
    def post(self, request):
        if not request.user.is_talent_admin():
            return R.failure(
                msg=_("Current users have no permission to modify"))
        value = request.data.get('value', '')
        parse_re = urlparse(value, scheme='http')
        if parse_re.scheme not in ('http', 'https') and parse_re.hostname in (
                '127.0.0.1', 'localhost'):
            return R.failure(msg=_("Parameter error"))
        profilefromdb = IastProfile.objects.filter(key='apiserver').first()
        if profilefromdb:
            profilefromdb.value = value
            profilefromdb.save()
            return R.success(msg=_("Created success"))
        profilefromdb = IastProfile.objects.create(key='apiserver',
                                                   value=value)
        profilefromdb.save()
        return R.success(msg=_("Created success"))
