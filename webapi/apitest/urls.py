######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : urls
# @created     : 星期三 1月 12, 2022 19:29:08 CST
#
# @description :
######################################################################



from django.conf.urls.static import static
from django.urls import include, path
import os
from webapi import settings
from apitest.views import (
    ApiTestHeaderEndpoint,
    ApiTestTriggerEndpoint,
    ApiTestOpenapiSpecEndpoint
)

urlpatterns = [
    path('project/<int:pk>/api_test/req_headers',
         ApiTestHeaderEndpoint.as_view()),
    path('project/<int:pk>/api_test', ApiTestTriggerEndpoint.as_view()),
    path('project/<int:pk>/api_test/openapi_spec',
         ApiTestOpenapiSpecEndpoint.as_view()),
]
urlpatterns = [path('api/v1/', include(urlpatterns))]
