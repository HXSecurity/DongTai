import json

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.version_control import VersionControl

# Create your views here.

COMPONENT_LIST = (
    "DongTai",
    "DongTai-agent-java",
    "DongTai-agent-python",
    "DongTai-engine",
    "DongTai-openapi",
    "DongTai-webapi",
)


class VersionListView(UserEndPoint):
    @extend_schema(summary="版本列表", tags=[_("Version List")])
    def get(self, request):
        component_datas = VersionControl.objects.filter(
            component_name__in=COMPONENT_LIST
        ).all()
        data = {}
        for component_data in component_datas:
            data[component_data.component_name] = {
                "version": component_data.version,
                "commit_hash": component_data.component_version_hash,
            }
            if not data[component_data.component_name]["commit_hash"]:
                del data[component_data.component_name]["commit_hash"]
            if component_data.additional:
                additional_data = json.loads(component_data.additional)
                data[component_data.component_name].update(additional_data)
        return R.success(data=data)
