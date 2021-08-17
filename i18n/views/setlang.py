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
        response = JsonResponse({'status': 201})
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
        )
        return response
