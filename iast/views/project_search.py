import logging

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project import IastProject
from iast.serializers.project import ProjectSerializer
from django.forms.models import model_to_dict

logger = logging.getLogger("django")

class ProjectSearch(UserEndPoint):
    '''
    项目名称搜索项目
    '''
    def get(self, request):
        name = request.query_params.get('name', '')
        size = request.query_params.get('size', 10)
        user = request.user
        size = int(size)
        projects = IastProject.objects.filter(
            user_id=user.id, name__icontains=name).order_by('-latest_time')[:size]
        data = [
            model_to_dict(project, fields=['id', 'name'])
            for project in projects
        ]
        return R.success(data=data)
