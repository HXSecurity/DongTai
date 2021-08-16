######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : setlang
# @created     : Thursday Aug 05, 2021 14:57:40 CST
#
# @description :
######################################################################

from dongtai.endpoint import R, AnonymousAndUserEndPoint
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
LANGUAGE_QUERY_PARAMETER = 'language'

class LanguageSetting(AnonymousAndUserEndPoint):
    def get(self, request):
        lang_code = request.GET.get(LANGUAGE_QUERY_PARAMETER)
        response = JsonResponse({})
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
        return response
