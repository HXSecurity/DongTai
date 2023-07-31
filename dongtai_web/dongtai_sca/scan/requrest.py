import json
import logging
from collections.abc import Callable
from http import HTTPStatus
from json.decoder import JSONDecodeError
from time import sleep
from urllib.parse import urljoin

import requests
from marshmallow.exceptions import ValidationError
from requests import Response
from requests.exceptions import ConnectionError, ConnectTimeout, RequestException
from result import Err, Ok, Result

from dongtai_common.common.utils import cached_decorator
from dongtai_conf.settings import SCA_BASE_URL, SCA_MAX_RETRY_COUNT, SCA_TIMEOUT
from dongtai_web.dongtai_sca.common.dataclass import PackageInfo, PackageResponse, PackageVulResponse, Vul

from .utils import get_sca_token

logger = logging.getLogger("dongtai-webapi")


def request_get_res_data_with_exception(
    data_extract_func: Callable[[Response], Result] = lambda x: Ok(x), *args, **kwargs
) -> Result:
    try:
        response: Response = requests.request(*args, **kwargs)
        max_retry_count = kwargs.get("max_retry_count", SCA_MAX_RETRY_COUNT)
        logger.debug(f"response content: {response.content!r}")
        logger.info(f"response content url: {response.url} status_code: {response.status_code}")
        if response.status_code == HTTPStatus.FORBIDDEN:
            return Err("Auth Failed")
        retry_count = 0
        while response.status_code == HTTPStatus.TOO_MANY_REQUESTS and retry_count < max_retry_count:
            retry_after = int(response.headers.get("Retry-After".lower(), 1))
            logger.info(
                f"response content url: {response.url} status_code: {response.status_code} retry_after: {retry_after} retry_count: {retry_count}"
            )
            sleep(retry_after)
            response = requests.request(*args, **kwargs)
            retry_count += 1
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            logger.warning(
                "Rate limte retry failed, please add retry count in config.ini or reduce concurrency in your celery worker about sca."
            )
            return Err("Rate Limit retry failed")
        res = data_extract_func(response)
        if isinstance(res, Err):
            return res
        return Ok(res.value)
    except (ConnectionError, ConnectTimeout):
        return Err("ConnectionError with target server")
    except JSONDecodeError:
        logger.debug(f"content decode error :{response.content!r}")
        logger.info("content decode error")
        return Err("Content decode error")
    except RequestException as e:
        logger.error(e, exc_info=True)
        return Err("Request Exception")
    except Exception as e:
        logger.error(e, exc_info=True)
        return Err("Exception")


def data_transfrom(response: Response) -> Result[list[dict], str]:
    if response.status_code == HTTPStatus.FORBIDDEN:
        return Err("Rate Limit Exceeded")
    try:
        res_data = json.loads(response.content)
        return Ok(res_data["data"])
    except JSONDecodeError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"JSONDecodeError content: {response.content!r}")
        return Err("Failed")
    except KeyError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"content form not match content: {response.content!r}")
        return Err("Failed")
    except Exception as e:
        logger.error(f"unexcepted Exception : {e}", exc_info=True)
        return Err("Failed")


def data_transfrom_package_v3(response: Response) -> Result[list[PackageInfo], str]:
    if response.status_code == HTTPStatus.FORBIDDEN:
        return Err("Auth Failed")
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        return Err("Rate Limit Exceeded")
    try:
        res_data = PackageResponse.from_json(response.content)
        return Ok(list(res_data.data))
    except ValidationError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"ValidationError content: {response.content!r}")
        return Err("Failed")
    except JSONDecodeError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"JSONDecodeError content: {response.content!r}")
        return Err("Failed")
    except KeyError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"content form not match content: {response.content!r}")
        return Err("Failed")
    except Exception as e:
        logger.error(f"unexcepted Exception : {e}", exc_info=True)
        logger.info(f"ValidationError content: {response.content!r}")
        return Err("Failed")


def data_transfrom_package_vul_v2(
    response: Response,
) -> Result[tuple[list[dict], list[dict]], str]:
    if response.status_code == HTTPStatus.FORBIDDEN:
        return Err("Rate Limit Exceeded")
    try:
        res_data = json.loads(response.content)
        return Ok((res_data["data"], res_data["safe_version"]))
    except JSONDecodeError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"JSONDecodeError content: {response.content!r}")
        return Err("Failed")
    except KeyError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"content form not match content: {response.content!r}")
        return Err("Failed")
    except Exception as e:
        logger.error(f"unexcepted Exception : {e}", exc_info=True)
        return Err("Failed")


def data_transfrom_package_vul_v3(
    response: Response,
) -> Result[tuple[tuple[Vul, ...], tuple[str, ...], tuple[str, ...]], str]:
    try:
        res_data = PackageVulResponse.from_json(response.content)
        return Ok(
            (
                res_data.data.vuls,
                tuple(res_data.data.affected_versions),
                tuple(res_data.data.unaffected_versions),
            )
        )
    except ValidationError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"ValidationError content: {response.content!r}")
        return Err("Failed")
    except JSONDecodeError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"JSONDecodeError content: {response.content!r}")
        return Err("Failed")
    except KeyError as e:
        logger.debug(e, exc_info=True)
        logger.info(f"content form not match content: {response.content!r}")
        return Err("Failed")
    except Exception as e:
        logger.error(f"unexcepted Exception : {e}", exc_info=True)
        return Err("Failed")


@cached_decorator(
    random_range=(2 * 60 * 60, 2 * 60 * 60),
)
def get_package_vul(aql: str = "", ecosystem: str = "", package_hash: str = "") -> list[dict]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v1/package_vul/")
    querystring = {"aql": aql} if aql else {"ecosystem": ecosystem, "hash": package_hash}
    headers = {"Token": get_sca_token()}
    payload = ""
    res = request_get_res_data_with_exception(
        data_transfrom,
        "GET",
        url,
        data=payload,
        params=querystring,
        headers=headers,
        timeout=SCA_TIMEOUT,
    )
    if isinstance(res, Err):
        return []
    return res.value


@cached_decorator(
    random_range=(2 * 60 * 60, 2 * 60 * 60),
)
def get_package_vul_v2(aql: str = "", ecosystem: str = "", package_hash: str = "") -> tuple[list[dict], list[dict]]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v2/package_vul/")
    querystring = {"aql": aql} if aql else {"ecosystem": ecosystem, "hash": package_hash}
    headers = {"Token": get_sca_token()}
    payload = ""
    res = request_get_res_data_with_exception(
        data_transfrom_package_vul_v2,
        "GET",
        url,
        data=payload,
        params=querystring,
        headers=headers,
        timeout=SCA_TIMEOUT,
    )
    if isinstance(res, Err):
        return [], []
    return res.value


@cached_decorator(
    random_range=(2 * 60 * 60, 2 * 60 * 60),
)
def get_package_vul_v4(
    aql: str = "",
    ecosystem: str = "",
    package_version: str = "",
    package_name: str = "",
) -> tuple[tuple[Vul, ...], tuple[str, ...], tuple[str, ...]]:
    url = urljoin(
        SCA_BASE_URL,
        f"/openapi/sca/v4/package/{ecosystem.lower()}/{package_name}/{package_version}/vuls",
    )
    headers = {"Token": get_sca_token()}
    payload = ""
    res = request_get_res_data_with_exception(
        data_transfrom_package_vul_v3,
        "GET",
        url,
        data=payload,
        headers=headers,
        timeout=SCA_TIMEOUT,
    )
    if isinstance(res, Err):
        return (), (), ()
    return res.value


@cached_decorator(
    random_range=(2 * 60 * 60, 2 * 60 * 60),
)
def get_package(aql: str = "", ecosystem: str = "", package_hash: str = "") -> list[dict]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v1/package/")
    querystring = {"aql": aql} if aql else {"ecosystem": ecosystem, "hash": package_hash}
    headers = {"Token": get_sca_token()}
    payload = ""
    res = request_get_res_data_with_exception(
        data_transfrom,
        "GET",
        url,
        data=payload,
        params=querystring,
        headers=headers,
        timeout=SCA_TIMEOUT,
    )
    if isinstance(res, Err):
        return []
    return res.value


@cached_decorator(
    random_range=(2 * 60 * 60, 2 * 60 * 60),
)
def get_package_v2(aql: str = "", ecosystem: str = "", package_hash: str = "") -> list[dict]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v1/package/")
    querystring = {"aql": aql} if aql else {"ecosystem": ecosystem, "hash": package_hash}
    headers = {"Token": get_sca_token()}
    payload = ""
    res = request_get_res_data_with_exception(
        data_transfrom,
        "GET",
        url,
        data=payload,
        params=querystring,
        headers=headers,
        timeout=SCA_TIMEOUT,
    )
    if isinstance(res, Err):
        return []
    return res.value


@cached_decorator(
    random_range=(2 * 60 * 60, 2 * 60 * 60),
)
def get_package_v3(aql: str = "", ecosystem: str = "", package_hash: str = "") -> list[PackageInfo]:
    url = urljoin(SCA_BASE_URL, f"/openapi/sca/v3/package/{ecosystem}/hash/{package_hash}")
    headers = {"Token": get_sca_token()}
    payload = ""
    res = request_get_res_data_with_exception(
        data_transfrom_package_v3,
        "GET",
        url,
        data=payload,
        headers=headers,
        timeout=SCA_TIMEOUT,
    )
    retry_count = 0
    while res.is_err() and res.value == "Rate Limit Exceeded" and retry_count < SCA_MAX_RETRY_COUNT:
        retry_count += 1
        res = request_get_res_data_with_exception(
            data_transfrom_package_v3,
            "GET",
            url,
            data=payload,
            headers=headers,
            timeout=SCA_TIMEOUT,
        )
    if isinstance(res, Err):
        return []
    return res.value
