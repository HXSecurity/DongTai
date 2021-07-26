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


    def post(self, request):
        """
        创建
        """
        value = request.data.get('value', '')
        profilefromdb = IastProfile.objects.filter(
            key='apiserver').first()
        if profilefromdb:
            profilefromdb.value = value
            profilefromdb.save()
            return R.success(msg="创建成功")
        profilefromdb = IastProfile.objects.create(key='openapi',value=value)
        profilefromdb.save()
        return R.success(msg="创建成功")
