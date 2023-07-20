#!/usr/bin/env python
from dongtai_common.endpoint import TalentAdminEndPoint, R
from django.utils.translation import gettext_lazy as _


class AgentUpgradeOffline(TalentAdminEndPoint):
    name = "api-v1-agent-offline-upgrade"
    description = _("Offline Upgrade Agent")

    def post(self, request):
        file = request.FILES["file"]
        status, filename = AgentUpgradeOffline.check_file(file.name)
        if status:
            AgentUpgradeOffline.handle_uploaded_file(filename, file)
            return R.success(msg=_("Upload successful"))
        return R.failure(msg=_("{} files not supported").format(filename))

    @staticmethod
    def handle_uploaded_file(filename, file):
        with open(f"iast/upload/iast-package/{filename}", "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    @staticmethod
    def check_file(filename):
        if filename in ["iast-agent.jar", "iast-core.jar", "iast-inject.jar"]:
            return True, filename
        return False, filename
