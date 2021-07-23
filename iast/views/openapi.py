from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from webapi.settings import config
from dongtai.models.profile import IastProfile


class OpenApiEndpoint(UserEndPoint):
    def get(self, request):
        """
        获取openapi配置
        """
        profilefromdb = IastProfile.objects.filter(
            key='apiserver').values_list('value', flat=True).first()
        profilefromini = config.get('apiserver', 'url')
        profiles = list(
            filter(lambda x: x is not None, [profilefromdb, profilefromini]))
        if profiles == []:
            return R.failure(msg="获取openapi配置失败")
        return R.success(data={'url': profiles[0]})
