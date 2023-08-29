#!/usr/bin/env python
# datetime: 2021/10/22 下午2:26
import time
import uuid
from http.client import BadStatusLine, HTTPResponse
from io import BytesIO

from celery.apps.worker import logger
from django.core.cache import cache
from django.db import IntegrityError

from dongtai_common.models.header_vulnerablity import (
    IastHeaderVulnerability,
    IastHeaderVulnerabilityDetail,
)
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils import const
from dongtai_engine.plugins import is_strategy_enable
from dongtai_engine.plugins.project_time_update import (
    project_time_stamp_update,
    project_version_time_stamp_update,
)
from dongtai_engine.signals import send_notify
from dongtai_web.vul_log.vul_log import log_vul_found


class FakeSocket:
    def __init__(self, response_str):
        self._file = BytesIO(response_str)

    def makefile(self, *args, **kwargs):
        return self._file


def parse_response(http_response_str):
    source = FakeSocket(http_response_str.encode())
    response = HTTPResponse(source)  # type:ignore
    response.begin()
    return response


def check_csp(response):
    if response.getheader("Content-Security-Policy") is None:
        return True
    return None


def check_x_xss_protection(response):
    if response.getheader("X-XSS-Protection") is None:
        return True
    if response.getheader("X-XSS-Protection").strip() == "0":
        return True
    return None


def check_strict_transport_security(response):
    if response.getheader("Strict-Transport-Security"):
        # parse max-age
        import re

        result = re.match("max-age=(\\d+);.*?", response.getheader("Strict-Transport-Security"))
        if result is None:
            return None
        max_age = result.group(1)
        if int(max_age) < 15768000:
            return True
        return None
    return None


def check_x_frame_options(response):
    if response.getheader("X-Frame-Options") is None:
        return True
    return None


def check_x_content_type_options(response):
    if response.getheader("X-Content-Type-Options") is None:
        return True
    return None


def check_response_header(method_pool):
    try:
        response = parse_response(method_pool.res_header.strip() + "\n\n" + method_pool.res_body.strip())
    except BadStatusLine as e:
        logger.debug("parse response header failed, reason: %s", e)
        return
    try:
        if check_csp(response):
            save_vul(
                "Response Without Content-Security-Policy Header",
                method_pool,
                position="HTTP Response Header",
            )
        if check_x_xss_protection(response):
            save_vul("Response With X-XSS-Protection Disabled", method_pool)
        if check_strict_transport_security(response):
            save_vul(
                "Response With Insecurely Configured Strict-Transport-Security Header",
                method_pool,
                position="HTTP Response Header",
            )
        if check_x_frame_options(response):
            save_vul(
                "Pages Without Anti-Clickjacking Controls",
                method_pool,
                position="HTTP Response Header",
            )
        if check_x_content_type_options(response):
            save_vul(
                "Response Without X-Content-Type-Options Header",
                method_pool,
                position="HTTP Response Header",
            )
    except Exception as e:
        logger.warning(
            "check_response_header failed, reason: " + str(e),
            exc_info=e,
        )


def save_vul(vul_type, method_pool, position="", data=""):
    if is_strategy_enable(vul_type, method_pool) is False:
        return
    vul_strategy = IastStrategyModel.objects.filter(
        vul_type=vul_type,
        state=const.STRATEGY_ENABLE,
        user_id__in=(1, method_pool.agent.user.id),
    ).first()
    if vul_strategy is None:
        logger.warning(f"There is no corresponding strategy for the current vulnerability: {vul_type}")

    from dongtai_common.models.agent import IastAgent

    IastAgent.objects.filter(project_version_id=method_pool.agent.project_version_id)
    uuid_key = uuid.uuid4().hex
    cache_key = f"vul_save-{vul_strategy.id}--{method_pool.http_method}-{method_pool.agent.project_version_id}"
    is_api_cached = uuid_key != cache.get_or_set(cache_key, uuid_key)

    if is_api_cached:
        return
    vul = (
        IastVulnerabilityModel.objects.filter(
            strategy_id=vul_strategy.id,
            uri="",
            http_method="",
            agent__project_version_id=method_pool.agent.project_version_id,
        )
        .order_by("-latest_time")
        .first()
    )
    timestamp = int(time.time())
    project_time_stamp_update.apply_async((method_pool.agent.bind_project_id,), countdown=5)
    project_version_time_stamp_update.apply_async((method_pool.agent.project_version_id,), countdown=5)
    if vul:
        vul.url = ""
        vul.req_header = method_pool.req_header
        vul.req_params = method_pool.req_params
        vul.req_data = method_pool.req_data
        vul.res_header = method_pool.res_header
        vul.res_body = method_pool.res_body
        vul.taint_value = data
        vul.taint_position = position
        vul.context_path = method_pool.context_path
        vul.client_ip = method_pool.clent_ip
        vul.counts = vul.counts + 1
        vul.latest_time = timestamp
        vul.method_pool_id = method_pool.id
        vul.language = method_pool.agent.language
        vul.save(
            update_fields=[
                "url",
                "req_header",
                "req_params",
                "req_data",
                "res_header",
                "res_body",
                "taint_value",
                "taint_position",
                "context_path",
                "client_ip",
                "counts",
                "latest_time",
                "method_pool_id",
                "latest_time_desc",
            ]
        )
    else:
        from dongtai_common.models.hook_type import HookType

        hook_type = HookType.objects.filter(vul_strategy_id=vul_strategy.id).first()
        vul = IastVulnerabilityModel.objects.create(
            strategy=vul_strategy,
            # fixme: remove field
            hook_type=hook_type if hook_type else HookType.objects.first(),
            level=vul_strategy.level,
            url="",
            uri="",
            http_method="",
            http_scheme=method_pool.http_scheme,
            http_protocol=method_pool.http_protocol,
            req_header=method_pool.req_header,
            req_params=method_pool.req_params,
            req_data=method_pool.req_data,
            res_header=method_pool.res_header,
            res_body=method_pool.res_body,
            full_stack="",
            top_stack="",
            bottom_stack="",
            taint_value=data,
            taint_position=position,
            agent=method_pool.agent,
            context_path=method_pool.context_path,
            counts=1,
            status_id=const.VUL_CONFIRMED,
            first_time=method_pool.create_time,
            latest_time=timestamp,
            client_ip=method_pool.clent_ip,
            param_name="",
            method_pool_id=method_pool.id,
            project_version_id=method_pool.agent.project_version_id,
            project_id=method_pool.agent.bind_project_id,
            language=method_pool.agent.language,
            server_id=method_pool.agent.server_id,
        )
        log_vul_found(
            vul.agent.user_id,
            vul.agent.bind_project.name,
            vul.agent.bind_project_id,
            vul.id,
            vul.strategy.vul_name,
        )  # type: ignore
        send_notify.send_robust(
            sender=save_vul,
            vul_id=vul.id,
            department_id=method_pool.agent.department_id,
        )
    cache.delete(cache_key)
    header_vul = None
    if not IastHeaderVulnerability.objects.filter(
        project_id=method_pool.agent.bind_project_id,
        project_version=method_pool.agent.project_version_id,
        url=method_pool.uri,
        vul=vul.id,
    ).exists():
        try:
            header_vul = IastHeaderVulnerability.objects.create(
                project_id=method_pool.agent.bind_project_id,
                project_version_id=method_pool.agent.project_version_id,
                url=method_pool.uri,
                vul_id=vul.id,
            )
        except IntegrityError:
            logger.debug("unique error stack: ", exc_info=True)
            logger.info("unique error cause by concurrency insert,ignore it")
    if (
        header_vul
        and not IastHeaderVulnerabilityDetail.objects.filter(
            agent_id=method_pool.agent_id,
            header_vul_id=header_vul.id,
        ).exists()
    ):
        try:
            IastHeaderVulnerabilityDetail.objects.create(
                agent_id=method_pool.agent_id,
                method_pool_id=method_pool.id,
                header_vul_id=header_vul.id,
                req_header=method_pool.req_header_fs,
                res_header=method_pool.res_header,
            )
        except IntegrityError:
            logger.debug("unique error stack: ", exc_info=True)
            logger.info("unique error cause by concurrency insert,ignore it")
    # delete if exists more than one   departured use redis lock
    # IastVulnerabilityModel.objects.filter(
    # ).delete()
