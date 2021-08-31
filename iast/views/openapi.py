from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from webapi.settings import config
from dongtai.models.profile import IastProfile
from django.utils.translation import gettext_lazy as _


class OpenApiEndpoint(UserEndPoint):
    def get(self, request):
        profilefromdb = IastProfile.objects.filter(
            key='apiserver').values_list('value', flat=True).first()
        profilefromini = None
        profiles = list(
            filter(lambda x: x is not None, [profilefromdb, profilefromini]))
        if profiles == [] or not profiles[0]:
            return R.failure(msg=_("Get OpenAPI configuration failed"))
        return R.success(data={'url': profiles[0]})


    def post(self, request):
        if not request.user.is_talent_admin():
            return R.failure(msg=_("Current users have no permission to modify"))
        value = request.data.get('value', '')
        profilefromdb = IastProfile.objects.filter(
            key='apiserver').first()
        if profilefromdb:
            profilefromdb.value = value
            profilefromdb.save()
            return R.success(msg=_("Created success"))
        profilefromdb = IastProfile.objects.create(key='apiserver',value=value)
        profilefromdb.save()
        return R.success(msg=_("Created success"))
