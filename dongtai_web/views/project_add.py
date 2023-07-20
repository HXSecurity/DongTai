#!/usr/bin/env python
import ipaddress
import logging
import time
from urllib.parse import urlparse, urlunparse

import requests
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.common.utils import disable_cache
from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.server import IastServer
from dongtai_common.models.strategy_user import IastStrategyUser
from dongtai_engine.common.queryset import get_scan_id
from dongtai_web.base.project_version import (
    version_modify,
)
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("django")


class _ProjectsAddBodyArgsSerializer(serializers.Serializer):
    name = serializers.CharField(help_text=_("The name of project"))
    template_id = serializers.IntegerField(
        help_text=_(
            "The id corresponding to the project template. required to specfic, use 1 as default."
        )
    )
    version_name = serializers.CharField(
        required=False, help_text=_("The version name of the project")
    )
    pid = serializers.IntegerField(
        required=False,
        help_text=_(
            "The id of the project, use it when try to modify existed project."
        ),
    )
    description = serializers.CharField(
        required=False, help_text=_("Description of the project")
    )
    vul_validation = serializers.IntegerField(
        help_text="vul validation switch",
    )
    base_url = serializers.CharField(
        required=False,
    )
    test_req_header_key = serializers.CharField(
        required=False,
    )
    test_req_header_value = serializers.CharField(
        required=False,
    )


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((202, _("Parameter error")), ""),
        ((201, _("Created success")), ""),
        ((202, _("Agent has been bound by other application")), ""),
        ((203, _("Failed to create, the application name already exists")), ""),
    )
)


class ProjectAdd(UserEndPoint):
    name = "api-v1-project-add"
    description = _("New application")

    @extend_schema_with_envcheck(
        request=_ProjectsAddBodyArgsSerializer,
        tags=[_("Project")],
        summary=_("Projects Add"),
        description=_(
            """Create a new project according to the given conditions;
            when specifying the project id, update the item corresponding to the id according to the given condition."""
        ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        try:
            with transaction.atomic():
                name = request.data.get("name")
                mode = "插桩模式"
                scan_id = int(request.data.get("scan_id", 5))
                template_id = int(request.data.get("template_id", 1))
                departments = request.user.get_relative_department()
                scan = IastStrategyUser.objects.filter(id=scan_id).first()
                base_url = request.data.get("base_url", None)
                test_req_header_key = request.data.get("test_req_header_key", None)
                test_req_header_value = request.data.get("test_req_header_value", None)
                description = request.data.get("description", None)
                department_id = request.data.get("department_id", None)
                pid = request.data.get("pid", 0)
                enable_log = request.data.get("enable_log", None)
                log_level = request.data.get("log_level", None)
                accessable_ips = []
                if pid and base_url:
                    ips = filter(
                        lambda x: ip_validate(x),
                        [
                            i[0]
                            for i in IastServer.objects.filter(pid=pid)
                            .values_list("ip")
                            .distinct()
                            .all()
                        ],
                    )
                    accessable_ips = _accessable_ips(base_url, ips)
                if accessable_ips:
                    parsed_url = urlparse(base_url)
                    if parsed_url.netloc not in parsed_url:
                        return R.failure(status=202, msg=_("base_url validate failed"))
                if base_url and not url_validate(base_url):
                    return R.failure(status=202, msg=_("base_url validate failed"))
                if not scan_id or not name or not mode:
                    logger.error("require base scan_id and name")
                    return R.failure(
                        status=202, msg=_("Required scan strategy and name")
                    )

                version_name = request.data.get("version_name", "")
                if not version_name:
                    version_name = "V1.0"
                vul_validation = request.data.get("vul_validation", None)

                if pid:
                    project = IastProject.objects.filter(
                        id=pid, department__in=departments
                    ).first()
                    project.name = name
                else:
                    department_id = request.data.get("department_id", 1)
                    if not departments.filter(pk=department_id).exists():
                        return R.failure(status=203, msg=_("department does not exist"))

                    project = IastProject.objects.filter(
                        name=name, user_id=request.user.id, department_id=department_id
                    ).first()
                    if not project:
                        project = IastProject.objects.create(
                            name=name,
                            user_id=request.user.id,
                            department_id=department_id,
                            template_id=template_id,
                        )
                    else:
                        return R.failure(
                            status=203,
                            msg=_(
                                "Failed to create, the application name already exists"
                            ),
                        )

                versionInfo = IastProjectVersion.objects.filter(
                    project_id=project.id, current_version=1, status=1
                ).first()
                project_version_id = versionInfo.id if versionInfo else 0
                current_project_version = {
                    "project_id": project.id,
                    "version_id": project_version_id,
                    "version_name": version_name,
                    "description": request.data.get("description", ""),
                    "current_version": 1,
                }
                if not versionInfo or not (
                    versionInfo.version_name == version_name
                    and (versionInfo.description == description or not description)
                ):
                    result = version_modify(
                        project.user, departments, current_project_version
                    )
                    if result.get("status", "202") == "202":
                        logger.error("version update failure")
                        return R.failure(
                            status=202, msg=result.get("msg", _("Version Update Error"))
                        )
                    project_version_id = result.get("data", {}).get("version_id", 0)

                project.scan = scan
                project.mode = mode
                project.template_id = template_id
                project.department_id = department_id
                project.latest_time = int(time.time())
                project.enable_log = enable_log
                project.log_level = log_level
                if vul_validation is not None:
                    project.vul_validation = vul_validation
                if base_url:
                    project.base_url = replace_ending(base_url, "/", "")
                if test_req_header_key:
                    project.test_req_header_key = test_req_header_key
                if test_req_header_value:
                    project.test_req_header_value = test_req_header_value
                project.save(
                    update_fields=[
                        "name",
                        "scan_id",
                        "mode",
                        "latest_time",
                        "vul_validation",
                        "base_url",
                        "test_req_header_key",
                        "test_req_header_value",
                        "template_id",
                        "department_id",
                        "enable_log",
                        "log_level",
                    ]
                )
                disable_cache(get_scan_id, (project.id))
                return R.success(
                    data={
                        "project_id": project.id,
                        "project_version_id": project_version_id,
                    },
                    msg="操作成功",
                )
        except Exception as e:
            logger.exception("uncatched exception: ", exc_info=e)
            return R.failure(status=202, msg=_("Parameter error"))


def _accessable_ips(url, ips):
    parse_re = urlparse(url)
    return list(
        filter(lambda x: url_accessable(urlunparse(parse_re._replace(netloc=x))), ips)
    )


def url_accessable(url):
    try:
        requests.get(url, timeout=2)
    except Exception:
        return False
    return True


def url_validate(url):
    parse_re = urlparse(url)
    if parse_re.scheme not in ("http", "https") or parse_re.hostname in (
        "127.0.0.1",
        "localhost",
    ):
        return False
    return ip_validate(parse_re.hostname) if is_ip(parse_re.hostname) else True


def ip_validate(ip):
    try:
        ipadrs = ipaddress.IPv4Address(ip)
        if (
            int(ipaddress.IPv4Address("127.0.0.1"))
            < int(ipadrs)
            < int(ipaddress.IPv4Address("127.255.255.255"))
        ):
            logger.error("127.x.x.x address not allowed")
            return False
        if (
            int(ipaddress.IPv4Address("10.0.0.1"))
            < int(ipadrs)
            < int(ipaddress.IPv4Address("10.255.255.255"))
        ):
            logger.error("10.x.x.x address not allowed")
            return False
    except ipaddress.AddressValueError:
        pass
    return True


def is_ip(address):
    return not address.split(".")[-1].isalpha()


def replace_ending(sentence, old, new):
    if sentence.endswith(old):
        return sentence[: -len(old)] + new
    return sentence
