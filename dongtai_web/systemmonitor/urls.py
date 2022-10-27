from django.urls import include, path

from rest_framework import routers
from dongtai_web.systemmonitor.data_clean import DataCleanEndpoint, DataCleanDoItNowEndpoint

from _typeshed import Incomplete
router: Incomplete = routers.DefaultRouter()

base_urlpatterns: Incomplete = [
    path('data_clean', DataCleanEndpoint.as_view()),
    path('data_clean/task', DataCleanDoItNowEndpoint.as_view()),
]

urlpatterns: Incomplete = [
    path('api/v1/systemmonitor/', include(base_urlpatterns)),
]
