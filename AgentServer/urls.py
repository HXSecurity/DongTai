"""AgentServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from AgentServer import settings

urlpatterns = [
    path('api/v1/', include('apiserver.urls'), name='OpenAPI'),
    path('sca/v1/', include('sca.urls'), name='ScaAPI'),
]

if settings.DEBUG:
    urlpatterns.extend(
        [
            path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
            path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
            path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ]
    )
