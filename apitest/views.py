from django.shortcuts import render

from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
# Create your views here.

class ApiTestEndpoint(UserEndPoint):
    def post(self,request):
        pass
