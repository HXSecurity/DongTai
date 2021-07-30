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
        size = int(request.query_params.get('size', 30))
        users = self.get_auth_users(request.user)
        projects = IastProject.objects.filter(
            user__in=users,
            name__icontains=name).order_by('-latest_time')[:size]
        data = [
            model_to_dict(project, fields=['id', 'name'])
            for project in projects
        ]
        return R.success(data=data)
