#!/usr/bin/env python
# datetime:2020/8/26 11:47
import logging

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.asset import Asset
from dongtai_common.models.vul_level import IastVulLevel
from django.utils.translation import get_language
from dongtai_web.serializers.sca import ScaSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from dongtai_conf import settings
import requests
import json
from dongtai_web.dongtai_sca.models import VulCveRelation

logger = logging.getLogger("dongtai-webapi")


class ScaDetailResponseDataVulsSerializers(serializers.Serializer):
    safe_version = serializers.CharField()
    vulcve = serializers.CharField()
    vulcwe = serializers.CharField()
    vulname = serializers.CharField()
    overview = serializers.CharField()
    teardown = serializers.CharField()
    reference = serializers.CharField()
    level = serializers.CharField()


class ScaDetailResponseDataSerializers(ScaSerializer):
    vuls = ScaDetailResponseDataVulsSerializers(many=True)

    class Meta:
        model = ScaSerializer.Meta.model
        fields = [*ScaSerializer.Meta.fields, "vuls"]


_ResponseSerializer = get_response_serializer(ScaDetailResponseDataSerializers())


class ScaDetailView(UserEndPoint):
    name = "api-v1-scas"
    description = ""

    @extend_schema_with_envcheck(
        [],
        [],
        [
            {
                "name": _("Get data sample"),
                "description": _(
                    "The aggregation results are programming language, risk level, vulnerability type, project"
                ),
                "value": {
                    "status": 201,
                    "msg": "success",
                    "data": {
                        "id": 12897,
                        "package_name": "log4j-to-slf4j-2.14.1.jar",
                        "version": "2.14.1",
                        "project_name": "demo",
                        "project_id": 67,
                        "project_version": "V1.0",
                        "language": "JAVA",
                        "agent_name": "Mac OS X-localhost-v1.0.0-d24bf703ca62499ebdd12770708296f5",
                        "signature_value": "ce8a86a3f50a4304749828ce68e7478cafbc8039",
                        "level": "INFO",
                        "level_type": 4,
                        "vul_count": 0,
                        "dt": 1631088844,
                        "vuls": [],
                    },
                },
            }
        ],
        tags=[_("Component")],
        summary=_("Component Detail"),
        description=_(
            "Get the details of the corresponding component by specifying the id."
        ),
        response_schema=_ResponseSerializer,
    )
    def get(self, request, id):
        user = request.user

        try:
            agents = self.get_auth_agents_with_user(user)
            asset = Asset.objects.filter(agent__in=agents, id=id).first()

            if asset is None:
                return R.failure(
                    msg=_("Components do not exist or no permission to access")
                )
            data = ScaSerializer(asset).data
            data["vuls"] = []

            search_query = ""
            if asset.agent.language == "JAVA":
                search_query = "hash=" + asset.signature_value
            elif asset.agent.language == "PYTHON":
                version = asset.version
                name = asset.package_name.replace("-" + version, "")
                search_query = "ecosystem={}&name={}&version={}".format(
                    "PyPI", name, version
                )
            if search_query != "":
                try:
                    url = settings.SCA_BASE_URL + "/package_vul/?" + search_query
                    resp = requests.get(url=url)
                    resp = json.loads(resp.content)
                    maven_model = resp.get("data", {}).get("package", {})
                    if maven_model is None:
                        maven_model = {}
                    vul_list = resp.get("data", {}).get("vul_list", [])

                    levels = IastVulLevel.objects.all()
                    level_dict = {}
                    language = get_language()
                    for level in levels:
                        if language == "zh":
                            level_dict[level.name] = level.name_value_zh
                        if language == "en":
                            level_dict[level.name] = level.name_value_en

                    for vul in vul_list:
                        _level = vul.get("vul_package", {}).get("severity", "none")
                        _vul = vul.get("vul", {})
                        _fixed_versions = vul.get("fixed_versions", [])
                        cwe_ids = vul.get("vul_package", {}).get("cwe_ids", [])
                        vul = {
                            "safe_version": ",".join(_fixed_versions)
                            if len(_fixed_versions) > 0
                            else _(
                                "Current version stopped for maintenance or it is not a secure version"
                            ),
                            "vulcve": _vul.get("aliases", [])[0]
                            if len(_vul.get("aliases", [])) > 0
                            else "",
                            "vulcwe": ",".join(cwe_ids),
                            "vulname": _vul.get("summary", ""),
                            "overview": _vul.get("summary", ""),
                            "teardown": _vul.get("details", ""),
                            "reference": _vul.get("references", []),
                            "level": level_dict.get(_level, _level),
                        }
                        cverelation = VulCveRelation.objects.filter(
                            cve=vul["vulcve"]
                        ).first()
                        vul["vulcve_url"] = (
                            f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={vul['vulcve']}"
                            if vul["vulcve"]
                            else ""
                        )
                        vul["vulcnnvd_url"] = ""
                        vul["vulcnvd_url"] = ""
                        vul["vulcnnvd"] = ""
                        vul["vulcnvd"] = ""
                        if cverelation:
                            vul["vulcnnvd_url"] = (
                                f"http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD={cverelation.cnnvd}"
                                if cverelation.cnnvd
                                else ""
                            )
                            vul["vulcnvd_url"] = (
                                f"https://www.cnvd.org.cn/flaw/show/{cverelation.cnvd}"
                                if cverelation.cnvd
                                else ""
                            )
                            vul["vulcnnvd"] = (
                                cverelation.cnnvd if cverelation.cnnvd else ""
                            )
                            vul["vulcnvd"] = (
                                cverelation.cnvd if cverelation.cnvd else ""
                            )
                        data["vuls"].append(vul)

                except Exception as e:
                    logger.info(f"get package_vul failed:{e}")
            return R.success(data=data)
        except Exception as e:
            logger.error(e)
            return R.failure(msg=_("Component information query failed"))
