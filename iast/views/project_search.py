import logging

from django.forms.models import model_to_dict
from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project import IastProject
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck

logger = logging.getLogger("django")


class ProjectSearch(UserEndPoint):

    @extend_schema_with_envcheck([{
        'name': "name",
        'type': str,
    }])
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
