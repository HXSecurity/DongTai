import logging

from django.forms.models import model_to_dict
from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project import IastProject

logger = logging.getLogger("django")


class ProjectSearch(UserEndPoint):
    """
    项目名称搜索项目
    """

    def get(self, request):
        name = request.query_params.get('name', '')
        users = self.get_auth_users(request.user)
        projects = IastProject.objects.filter(
            user__in=users,
            name__icontains=name).order_by('-latest_time')
        data = [
            model_to_dict(project, fields=['id', 'name'])
            for project in projects
        ]
        return R.success(data=data)
