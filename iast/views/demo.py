######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : demo
# @created     : Wednesday Aug 04, 2021 15:00:46 CST
#
# @description :
######################################################################

from dongtai.endpoint import R, UserEndPoint
from dongtai.models.user import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.conf import settings


class Demo(UserEndPoint):
    permission_classes = []
    authentication_classes = []
    name = "user_views_login"
    description = "用户登录"

    def get(self, request):
        user = User.objects.filter(username="demo").first()
        login(request, user)
        res = HttpResponseRedirect(settings.DOMAIN + "project/projectManage")
        res.set_cookie(
            settings.SESSION_COOKIE_NAME,
            request.session.session_key,
            None,
            None,
            domain=settings.DEMO_SESSION_COOKIE_DOMAIN,
        )
        res.set_cookie(
            settings.CSRF_COOKIE_NAME,
            request.META['CSRF_COOKIE'],
            None,
            None,
            domain=settings.DEMO_SESSION_COOKIE_DOMAIN,
        )
        return res
