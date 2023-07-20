######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : setlang
# @created     : Thursday Aug 05, 2021 14:57:40 CST
#
# @description :
######################################################################

from dongtai_common.endpoint import R, AnonymousAndUserEndPoint
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from dongtai_web.utils import extend_schema_with_envcheck
from dongtai_conf.settings import LANGUAGES
from django.utils.translation import gettext_lazy as _

LANGUAGE_QUERY_PARAMETER = "language"

ALLOWED_LANG_CODE = [x[0] for x in LANGUAGES]


class LanguageSetting(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck(
        [
            {
                "name": LANGUAGE_QUERY_PARAMETER,
                "type": str,
                "description": "The options are (en,zh)",
            }
        ],
        tags=["i18n"],
        summary="切换语言",
    )
    def get(self, request):
        lang_code = request.GET.get(LANGUAGE_QUERY_PARAMETER)
        if lang_code not in ALLOWED_LANG_CODE:
            return R.failure(msg=_("this language not supported now"))
        response = JsonResponse({"status": 201})
        if request.user.is_authenticated:
            user = request.user
            user.default_language = lang_code
            user.save()
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
        )
        return response


#
#
# class DefaultLanguageSetting(AnonymousAndUserEndPoint):
#    def post(self, request):
#        with open(CONFIGPATH, 'w') as configfile:
#
#    def get(self, request):
