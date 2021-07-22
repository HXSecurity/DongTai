import logging

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project import IastProject
from iast.serializers.project import ProjectSerializer


logger = logging.getLogger("django")

class ProjectsSearch(UserEndPoint):
    '''
    项目名称搜索项目
    '''

    def get(self, request):
        name = request.query_params.get('name', '')
        size = request.query_params.get('size', 10)
        user = request.user

        query_set = IastProject.objects.filter(
            user_id=user.id, name__icontains=name).values(
                'id', 'name').order_by('-latest_time')[:size]

        return R.success(data=ProjectSerializer(query_set, many=True).data)
