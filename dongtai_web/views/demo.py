######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : demo
# @created     : Wednesday Aug 04, 2021 15:00:46 CST
#
# @description :
######################################################################

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.user import User


class Demo(UserEndPoint):
    permission_classes = ()
    authentication_classes = ()
    name = "user_views_login"
    description = "用户登录"

    def get(self, request):
        user = User.objects.filter(username="demo").first()
        login(request, user)
        return HttpResponseRedirect(settings.DOMAIN + "project/projectManage")
