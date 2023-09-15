#!/usr/bin/env python
# datetime:2021/1/5 下午12:36
import base64
import gzip
import json
import logging
import time
import uuid
from datetime import datetime, timedelta
from hashlib import sha1, sha256

from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned
from django.db.utils import IntegrityError
from django.http.request import QueryDict

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.api_route import (
    IastApiMethod,
    IastApiParameter,
    IastApiRoute,
)
from dongtai_common.models.api_route_v2 import IastApiRouteV2
from dongtai_common.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_common.models.res_header import (
    HeaderType,
    ProjectSaasMethodPoolHeader,
)
from dongtai_common.utils import const
from dongtai_conf import settings
from dongtai_engine.tasks import (
    search_vul_from_method_pool,
    search_vul_from_replay_method_pool,
)
from dongtai_protocol import utils
from dongtai_protocol.report.handler.report_handler_interface import (
    IReportHandler,
    get_agent,
)
from dongtai_protocol.report.report_handler_factory import ReportHandler

logger = logging.getLogger("dongtai.openapi")


class A:
    ignored = False


@ReportHandler.register(const.REPORT_VULN_SAAS_POOL)
class SaasMethodPoolHandler(IReportHandler):
    def __init__(self):
        super().__init__()
        self.async_send = settings.config.getboolean("task", "async_send", fallback=False)
        self.async_send_delay = settings.config.getint("task", "async_send_delay", fallback=2)
        self.retryable = settings.config.getboolean("task", "retryable", fallback=False)

        if self.async_send and (ReportHandler.log_service_disabled or ReportHandler.log_service is None):
            logger.warning("log service disabled or failed to connect, disable async send method pool")
            self.async_send = False
        else:
            self.log_service = ReportHandler.log_service

    @staticmethod
    def parse_headers(headers_raw):
        headers = {}
        header_raw = base64.b64decode(headers_raw).decode("utf-8").split("\n")
        item_length = len(header_raw)
        for index in range(item_length):
            _header_list = header_raw[index].split(":")
            _header_name = _header_list[0]
            headers[_header_name] = ":".join(_header_list[1:])
        return headers

    def parse(self):
        self.version = self.report.get("version", "v1")
        self.http_uri = self.detail.get("uri")
        self.http_url = self.detail.get("url")
        self.http_query_string = self.detail.get("queryString")
        self.http_req_data = self.detail.get("reqBody")
        self.http_req_header = self.detail.get("reqHeader")
        self.http_method = self.detail.get("method")
        self.http_scheme = self.detail.get("scheme")
        self.http_secure = self.detail.get("secure")
        self.http_protocol = self.detail.get("protocol")
        self.http_replay = self.detail.get("replayRequest")
        self.http_res_header = self.detail.get("resHeader")
        self.http_res_body = self.detail.get("resBody")
        self.context_path = self.detail.get("contextPath")
        self.client_ip = self.detail.get("clientIp")
        self.method_pool = self.report.get("detail", {}).get("pool", None)
        if self.method_pool:
            self.method_pool = sorted(self.method_pool, key=lambda e: e.__getitem__("invokeId"), reverse=True)
        logger.info(f"start record method_pool : {self.agent_id} {self.http_uri} {self.http_method}")

    def save(self):
        """
        如果agent存在,保存数据
        :return:
        """
        headers = SaasMethodPoolHandler.parse_headers(self.http_req_header)
        import base64

        get_params_dict(
            base64.b64decode(self.http_req_header),
            self.http_req_data,
            self.http_query_string,
        )
        # update_api_route_deatil(self.agent_id, self.http_uri, self.http_method,
        #                        params_dict)
        add_new_api_route(self.agent, self.http_uri, self.http_method)
        if self.http_replay:
            # 保存数据至重放请求池
            replay_id = headers.get("dongtai-replay-id")
            replay_type = headers.get("dongtai-replay-type")
            relation_id = headers.get("dongtai-relation-id")
            timestamp = int(time.time())

            # fixme 直接查询replay_id是否存在,如果存在,直接覆盖
            query_set = IastAgentMethodPoolReplay.objects.values("id").filter(replay_id=replay_id)
            if query_set.exists():
                # 更新
                replay_model = query_set.first()
                replay_model.update(
                    url=self.http_url,
                    uri=self.http_uri,
                    req_header=self.http_req_header,
                    req_params=self.http_query_string,
                    req_data=self.http_req_data,
                    res_header=self.http_res_header,
                    res_body=new_decode_content(
                        self.http_res_body,
                        get_content_encoding(self.http_res_header),
                        self.version,
                    ),
                    context_path=self.context_path,
                    method_pool=json.dumps(self.method_pool),
                    clent_ip=self.client_ip,
                    update_time=timestamp,
                )
                method_pool_id = replay_model["id"]
            else:
                # 新增
                replay_model = IastAgentMethodPoolReplay.objects.create(
                    agent=self.agent,
                    url=self.http_url,
                    uri=self.http_uri,
                    http_method=self.http_method,
                    http_scheme=self.http_scheme,
                    http_protocol=self.http_protocol,
                    req_header=self.http_req_header,
                    req_params=self.http_query_string,
                    req_data=self.http_req_data,
                    res_header=self.http_res_header,
                    res_body=new_decode_content(
                        self.http_res_body,
                        get_content_encoding(self.http_res_header),
                        self.version,
                    ),
                    context_path=self.context_path,
                    method_pool=json.dumps(self.method_pool),
                    clent_ip=self.client_ip,
                    replay_id=replay_id,
                    replay_type=replay_type,
                    relation_id=relation_id,
                    create_time=timestamp,
                    update_time=timestamp,
                )
                method_pool_id = replay_model.id
            IastReplayQueue.objects.filter(id=replay_id).update(state=const.SOLVED)
            if method_pool_id:
                logger.info(f"send replay method pool {self.agent_id} {self.http_uri} {method_pool_id} to celery ")
                self.send_to_engine(method_pool_id=method_pool_id, model="replay")
        else:
            pool_sign = uuid.uuid4().hex
            if self.async_send:
                try:
                    method_pool = self.to_json(pool_sign)
                    ok = self.log_service.send(method_pool)
                    if ok:
                        self.send_to_engine(method_pool_sign=pool_sign)
                except Exception as e:
                    logger.warning(e, exc_info=True)
            else:
                current_version_agents = self.get_project_agents(self.agent)
                try:
                    update_record, method_pool = self.save_method_call(pool_sign, current_version_agents)
                except Exception as e:
                    logger.info(f"record method failed : {self.agent_id} {self.http_uri} {self.http_method}")
                    logger.warning(e, exc_info=e)
                try:
                    logger.info(f"send normal method pool {self.agent_id} {self.http_uri} {pool_sign} to celery ")
                    self.send_to_engine(method_pool_sign=pool_sign, update_record=update_record)
                except Exception as e:
                    logger.warning(e, exc_info=e)

    def to_json(self, pool_sign: str):
        timestamp = int(time.time())
        pool = {
            "agent_id": self.agent_id,
            "url": self.http_url,
            "uri": self.http_uri,
            "http_method": self.http_method,
            "http_scheme": self.http_scheme,
            "http_protocol": self.http_protocol,
            "req_header": self.http_req_header,
            "req_params": self.http_query_string,
            "req_data": self.http_req_data,
            "req_header_for_search": utils.build_request_header(
                req_method=self.http_method,
                raw_req_header=self.http_req_header,
                uri=self.http_uri,
                query_params=self.http_query_string,
                http_protocol=self.http_protocol,
            ),
            "res_header": utils.base64_decode(self.http_res_header),
            "res_body": new_decode_content(
                self.http_res_body,
                get_content_encoding(self.http_res_header),
                self.version,
            ),
            "context_path": self.context_path,
            "method_pool": json.dumps(self.method_pool),
            "pool_sign": pool_sign,
            "clent_ip": self.client_ip,
            "create_time": timestamp,
            "update_time": timestamp,
            "uri_sha1": self.sha1(self.http_uri),
            "user_id": self.agent.user_id,
            "bind_project_id": self.agent.bind_project_id,
            "project_version_id": self.agent.project_version_id,
            "language": self.agent.language,
        }
        return json.dumps(pool)

    def save_method_call(self, pool_sign: str, current_version_agents) -> tuple[bool, MethodPool]:
        """
        保存方法池数据
        :param pool_sign:
        :param current_version_agents:
        :return:
        """
        # todo need to del
        #            pool_sign=pool_sign, agent__in=current_version_agents).first()
        #        if method_pool:
        #            method_pool.req_header_fs = utils.build_request_header(
        #                http_protocol=self.http_protocol)
        #            method_pool.res_body = new_decode_content(
        #                self.version)
        #            method_pool.save(update_fields=[
        #                'update_time',
        #                'method_pool',
        #                'uri',
        #                'url',
        #                'http_method',
        #                'req_header',
        #                'req_params',
        #                'req_data',
        #                'req_header_fs',
        #                'res_header',
        #                'res_body',
        #                'uri_sha1',
        # 获取agent
        update_record = False
        try:
            timestamp = int(time.time())
            method_pool = MethodPool.objects.create(
                agent=self.agent,
                url=self.http_url,
                uri=self.http_uri,
                http_method=self.http_method,
                http_scheme=self.http_scheme,
                http_protocol=self.http_protocol,
                req_header=self.http_req_header,
                req_params=self.http_query_string,
                req_data=self.http_req_data,
                req_header_fs=utils.build_request_header(
                    req_method=self.http_method,
                    raw_req_header=self.http_req_header,
                    uri=self.http_uri,
                    query_params=self.http_query_string,
                    http_protocol=self.http_protocol,
                ),
                res_header=utils.base64_decode(self.http_res_header),
                res_body=new_decode_content(
                    self.http_res_body,
                    get_content_encoding(self.http_res_header),
                    self.version,
                ),
                context_path=self.context_path,
                method_pool=json.dumps(self.method_pool),
                pool_sign=pool_sign,
                clent_ip=self.client_ip,
                create_time=timestamp,
                update_time=timestamp,
                uri_sha1=self.sha1(self.http_uri),
            )
        except (IntegrityError, MultipleObjectsReturned) as e:
            logger.info(e)
            logger.debug(e, exc_info=e)
        return update_record, method_pool

    def send_to_engine(self, method_pool_id="", method_pool_sign="", update_record=False, model=None):
        try:
            if model is None:
                logger.info(
                    f'[+] send method_pool [{method_pool_sign}] to engine for {"update" if update_record else "new record"}'
                )
                delay = 0
                if self.async_send:
                    delay = self.async_send_delay
                kwargs = {
                    "method_pool_sign": method_pool_sign,
                    "agent_id": self.agent_id,
                    "retryable": self.retryable,
                }
                search_vul_from_method_pool.AsyncResult = lambda x: A()
                search_vul_from_method_pool.apply_async(
                    kwargs=kwargs,
                    countdown=delay,
                    expires=datetime.now() + timedelta(hours=3),
                    ignore_result=True,
                )
                # logger.info(
                #    f'[+] send method_pool [{method_pool_sign}] to engine for task search_vul_from_method_pool id: {res.task_id}')
            else:
                logger.info(f'[+] send method_pool [{method_pool_id}] to engine for {model if model else ""}')
                search_vul_from_replay_method_pool.delay(method_pool_id)
                # logger.info(
        except Exception as e:
            logger.exception(
                f"[-] Failure: send method_pool [{method_pool_id}{method_pool_sign}], Error: ",
                exc_info=e,
            )

    def calc_hash(self):
        sign_raw = "-".join(
            filter(
                lambda x: x,
                [
                    getattr(self, i, "")
                    for i in (
                        "http_uri",
                        "http_method",
                        "http_req_header",
                        "http_req_params",
                        "http_req_data",
                    )
                ],
            )
        )
        for method in self.method_pool:
            sign_raw += f"{method.get('className')}.{method.get('methodName')}()->"
        return self.sha256(sign_raw)

    @staticmethod
    def sha1(raw):
        h = sha1(usedforsecurity=False)
        h.update(raw.encode("utf-8"))
        return h.hexdigest()

    @staticmethod
    def sha256(raw):
        h = sha256(usedforsecurity=False)
        h.update(raw.encode("utf-8"))
        return h.hexdigest()

    def get_agent(self, agent_id):
        return get_agent(
            agent_id,
            {
                "pk": agent_id,
                "online": 1,
                "allow_report": 1,
            },
            (
                "id",
                "bind_project_id",
                "project_version_id",
                "project_name",
                "language",
                "project_version_id",
                "server_id",
                "filepathsimhash",
                "servicetype",
                "user_id",
            ),
        )


def save_project_header(keys: list, agent_id: int):
    uuid_key = uuid.uuid4().hex
    keys = list(
        filter(
            lambda key: uuid_key == cache.get_or_set(f"project_header-{agent_id}-{key}", uuid_key, 60 * 5),
            keys,
        )
    )
    objs = [ProjectSaasMethodPoolHeader(key=key, agent_id=agent_id, header_type=HeaderType.REQUEST) for key in keys]
    if not keys:
        return
    ProjectSaasMethodPoolHeader.objects.bulk_create(objs, ignore_conflicts=True)


def add_new_api_route(agent: IastAgent, path, method):
    logger.info(f"{agent.id}, {path}, {method}")
    uuid_key = uuid.uuid4().hex
    is_api_cached = uuid_key != cache.get_or_set(f"api_route-{agent.id}-{path}-{method}", uuid_key, 60 * 5)
    if is_api_cached:
        logger.info(f"found cache api_route-{agent.id}-{path}-{method} ,skip its insert")
        return
    try:
        IastApiRouteV2.objects.filter(
            path=path,
            method=method.lower(),
            project_id=agent.bind_project_id,
            project_version_id=agent.project_version_id,
        ).update(is_cover=1)
    except (IntegrityError, MultipleObjectsReturned) as e:
        logger.info(e)
        logger.debug(e, exc_info=e)


def get_params_dict(req_header, req_body, req_params):
    try:
        from dongtai_engine.filters.utils import parse_headers_dict_from_bytes

        res = parse_headers_dict_from_bytes(req_header)
        req_header_keys = list(filter(lambda x: x.upper() == "cookie", res.keys()))
    except BaseException:
        req_header_keys = []
    try:
        from http.cookies import SimpleCookie

        cookie = SimpleCookie()
        cookie.load(res["cookie"])
        cookie_keys = list(cookie.keys())
    except BaseException:
        cookie_keys = []
    try:
        body_keys = list(json.loads(req_body).keys())
    except BaseException:
        body_keys = []
    try:
        query_keys = list(QueryDict(req_params).keys())
    except BaseException:
        query_keys = []
    return {
        "header": req_header_keys,
        "cookie": cookie_keys,
        "jsonbody": body_keys,
        "query": query_keys,
    }


def update_api_route_deatil(agent_id, path, method, params_dict):
    annotation_dict = {
        "query": "GET请求参数",
        "cookie": "Cookie参数",
        "header": "Header参数",
        "jsonbody": "POST的json参数",
    }
    api_method, is_create = IastApiMethod.objects.get_or_create(method=method.upper())
    api_route = IastApiRoute.objects.filter(agent_id=agent_id, path=path, method_id=api_method.id).first()
    for key, value in params_dict.items():
        annotation = annotation_dict[key]
        for param_name in value:
            single_insert(api_route.id, param_name, annotation)


def single_insert(api_route_id, param_name, annotation) -> None:
    logger.info(f"{api_route_id}, {param_name}, {annotation}")
    uuid_key = uuid.uuid4().hex
    is_api_cached = uuid_key != cache.get_or_set(f"api_route_param-{api_route_id}-{param_name}", uuid_key, 60 * 5)
    if is_api_cached:
        logger.info(f"found cache api_route_param-{api_route_id}-{param_name}-{annotation} ,skip its insert")
        return
    try:
        param, _ = IastApiParameter.objects.get_or_create(
            route_id=api_route_id, name=param_name, defaults={"annotation": annotation}
        )
    except IntegrityError as e:
        logger.info(e)


def decode_content(body: bytes, content_encoding: str, version: str) -> str:
    if content_encoding == "gzip":
        try:
            return gzip.decompress(body).decode("utf-8")
        except BaseException:
            logger.warning("not gzip type but using gzip as content_encoding")
    # TODO not content_encoding
    if content_encoding:
        logger.info(f"not found content_encoding :{content_encoding}")
    try:
        return body.decode("utf-8")
    except BaseException:
        logger.info(f"decode_content, {body!r}")
        logger.info("utf-8 decode failed, use raw ")
        return body.decode("raw_unicode_escape")


def get_content_encoding(b64_res_headers: str) -> str:
    res_headers = utils.base64_decode(b64_res_headers)
    for header in res_headers.split("\n"):
        try:
            k, v = (i.strip().lower() for i in header.split(":"))
            if k == "content-encoding":
                if "gzip" in v:
                    return "gzip"
                break
        except BaseException:
            pass
    return ""


def get_res_body(res_body, version):
    if version == "v1":
        return res_body  # bytes
    if version == "v2":
        return base64.b64decode(res_body)  # bytes
    if version == "v3":
        return base64.b64decode(res_body)
    logger.info(f"no match version now version: {version}")
    return res_body


def new_decode_content(res_body: str, encoding: str, version: str) -> str:
    if version == "v1":
        return res_body
    if version in ("v2", "v3"):
        return decode_content(base64.b64decode(res_body), encoding, version)
    logger.info(f"no match version now version: {version}")
    return ""
