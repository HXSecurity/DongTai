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
from dongtai_conf import settings

from _typeshed import Incomplete
from dongtai_web.apitimelog.views import ApiTimeLogView as ApiTimeLogView
urlpatterns: Incomplete = [
]

if os.getenv('REQUESTLOG', None) == 'TRUE' or os.getenv('environment',
                                                        None) in ('TEST', ):
    from dongtai_web.apitimelog.views import ApiTimeLogView
    urlpatterns.extend([
        path('apitimelog', ApiTimeLogView.as_view()),
    ])

urlpatterns = [path('api/v1/', include(urlpatterns))]
