from django.urls import include, path

from rest_framework import routers
from dongtai_web.systemmonitor.data_clean import DataCleanEndpoint, DataCleanDoItNowEndpoint

router = routers.DefaultRouter()

base_urlpatterns = [
    path('data_clean', DataCleanEndpoint.as_view()),
    path('data_clean/task', DataCleanDoItNowEndpoint.as_view()),
]

urlpatterns = [
    path('api/v1/systemmonitor/', include(base_urlpatterns)),
]
