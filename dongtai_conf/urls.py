"""dongtai_conf URL Configuration

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
from django.conf.urls.static import static
from django.urls import include, path
import os
from dongtai_conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import URLPattern, URLResolver

urlpatterns: list[URLResolver | URLPattern] = [
    path('', include('{}.urls'.format(app))) for app in settings.CUSTOM_APPS
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns.extend([
    path('api/XZPcGFKoxYXScwGjQtJx8u/schema/',
            SpectacularJSONAPIView.as_view(),
            name='schema'),
    path('api/XZPcGFKoxYXScwGjQtJx8u/schema/swagger-ui/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui'),
    path('api/XZPcGFKoxYXScwGjQtJx8u/schema/redoc/',
            SpectacularRedocView.as_view(url_name='schema'),
            name='redoc'),
])

if os.getenv('DJANGOSILK', None) == 'TRUE':
    silk_path = os.getenv(
        'DJANGOSILKPATH',
        "9671ccbd0c655fda78354dda754c9c4fb7111b7c18751b25ea8930ab87c84f94")
    urlpatterns += [
        path(f"api/silk/{silk_path}/silk/", include('silk.urls', namespace='silk'))
    ]
