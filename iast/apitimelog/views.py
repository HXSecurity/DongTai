from apitimelog.middleware import REQUEST_DICT
# Create your views here.

from dongtai.endpoint import UserEndPoint
from django.http import JsonResponse


class ApiTimeLogView(UserEndPoint):
    def get(self, request):
        res = []
        for k,v in REQUEST_DICT.items():
            v['uri'] = k
            res.append(v)
        return JsonResponse(res,safe=False)
