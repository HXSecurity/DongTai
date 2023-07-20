######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : urls
# @created     : 星期三 1月 12, 2022 19:29:08 CST
#
# @description :
######################################################################


import os

from django.urls import include, path

urlpatterns = []

if os.getenv("REQUESTLOG", None) == "TRUE" or os.getenv("environment", None) in (
    "TEST",
):
    from dongtai_web.apitimelog.views import ApiTimeLogView

    urlpatterns.extend(
        [
            path("apitimelog", ApiTimeLogView.as_view()),
        ]
    )

urlpatterns = [path("api/v1/", include(urlpatterns))]
