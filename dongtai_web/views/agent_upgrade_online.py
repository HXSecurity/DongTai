#!/usr/bin/env python
from urllib.parse import urljoin

import requests
from dongtai_common.endpoint import TalentAdminEndPoint, R
from dongtai_common.models import User
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class AgentUpgradeArgsSerializer(serializers.Serializer):
    url = serializers.CharField(
        help_text=_("The resource link corresponding to the Agent.")
    )
    token = serializers.CharField(
        help_text=_(
            "The Token corresponding to the user is the same as when connecting to openapi."
        )
    )


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Online upgrade successful")), ""),
        (
            (
                202,
                _(
                    "Token verification failed, please confirm your input address and token are correct"
                ),
            ),
            "",
        ),
    )
)


class AgentUpgradeOnline(TalentAdminEndPoint):
    name = "api-v1-agent-install"
    description = _("Online Upgrade Agent")

    @extend_schema_with_envcheck(
        request=AgentUpgradeArgsSerializer,
        tags=[_("Agent")],
        summary=_("Agent Upgrade Online"),
        description=_("Agent upgrade"),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        url = request.data["url"]
        token = request.data["token"]
        try:
            self.download(url, token)
            User.objects.filter(id=request.user.id).update(upgrade_url=url)
            return R.success(msg=_("Online upgrade successful"))
        except Exception:
            return R.failure(
                msg=_(
                    "Token verification failed, please confirm your input address and token are correct"
                )
            )

    def token_verify(self, url, token):
        req_url = urljoin(url, "token/verify")
        resp = requests.get(req_url, headers={"Authorization": f"Token {token}"})
        return resp.status_code == 200 and resp.json()["status"] == 201

    def download(self, url, token):
        headers = {"Authorization": f"Token {token}"}
        resp = requests.get(url=urljoin(url, "iast-agent.jar"), headers=headers)
        with open("iast/upload/iast-package/iast-agent.jar", "wb") as f:
            f.write(resp.content)

        resp = requests.get(url=urljoin(url, "iast-inject.jar"), headers=headers)
        with open("iast/upload/iast-package/iast-inject.jar", "wb") as f:
            f.write(resp.content)

        resp = requests.get(url=urljoin(url, "iast-core.jar"), headers=headers)
        with open("iast/upload/iast-package/iast-core.jar", "wb") as f:
            f.write(resp.content)
