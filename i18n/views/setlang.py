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
from iast.utils import extend_schema_with_envcheck

LANGUAGE_QUERY_PARAMETER = 'language'


class LanguageSetting(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck([{
        'name': LANGUAGE_QUERY_PARAMETER,
        'type': str,
        'description': 'The options are (en,zh)'
    }])
    def get(self, request):
        lang_code = request.GET.get(LANGUAGE_QUERY_PARAMETER)
        response = JsonResponse({'status': 201})
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
        )
        return response
