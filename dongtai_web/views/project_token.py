from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_web.utils import extend_schema_with_envcheck


class ProjectToken(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Project")],
        summary=_("Projects Token"),
        description=_(
            "Get project information by project id, including the current version information of the project."
        ),
    )
    def get(self, request, pk):
        project = request.user.get_projects().filter(pk=pk).first()
        if project:
            return R.success(
                data={
                    "id": project.id,
                    "token": f"PROJECT{project.token}",
                }
            )
        return R.failure(status=203, msg=_("no permission"))
