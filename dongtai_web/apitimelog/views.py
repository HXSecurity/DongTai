from django.http import JsonResponse

# Create your views here.
from dongtai_common.endpoint import UserEndPoint
from dongtai_web.apitimelog.middleware import REQUEST_DICT


class ApiTimeLogView(UserEndPoint):
    def get(self, request):
        res = []
        for k, v in REQUEST_DICT.items():
            v["uri"] = k
            res.append(v)
        return JsonResponse(res, safe=False)
