from apitimelog.middleware import REQUEST_DICT
# Create your views here.

from dongtai.endpoint import UserEndPoint
from django.http import JsonResponse


class ApiTimeLogView(UserEndPoint):
    def get(self, request):
        return JsonResponse(REQUEST_DICT)
