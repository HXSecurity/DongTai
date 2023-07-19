import json
import logging
import time
from collections import defaultdict
from collections.abc import Callable
from hashlib import sha1
from http import HTTPStatus
from json.decoder import JSONDecodeError
from time import sleep
from urllib.parse import urljoin

import requests
from celery import shared_task
from django.db import IntegrityError
from packaging.version import _BaseVersion
from requests import Response
from requests.exceptions import ConnectionError, ConnectTimeout, RequestException
from result import Err, Ok, Result

from dongtai_common.common.utils import cached_decorator
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.asset import Asset
from dongtai_common.models.asset_vul import (
    IastAssetVul,
    IastAssetVulRelationMetaData,
    IastAssetVulType,
    IastAssetVulTypeRelation,
    IastVulAssetRelation,
)
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_conf.settings import (
    SCA_BASE_URL,
    SCA_MAX_RETRY_COUNT,
    SCA_SETUP,
    SCA_TIMEOUT,
)
from dongtai_web.dongtai_sca.models import PackageLicenseLevel

from .cwe import get_cwe_name

logger = logging.getLogger("dongtai-webapi")


def get_sca_token() -> str:
    #    'value', flat=True).first()
    # if profilefromdb:
    from dongtai_conf.settings import SCA_TOKEN

    return SCA_TOKEN


def request_get_res_data_with_exception(
    data_extract_func: Callable[[Response], Result] = lambda x: Ok(x), *args, **kwargs
) -> Result:
    try:
        response: Response = requests.request(*args, **kwargs)
        max_retry_count = kwargs.get("max_retry_count", SCA_MAX_RETRY_COUNT)
        logger.debug(f"response content: {response.content!r}")
        logger.info(
            f"response content url: {response.url} status_code: {response.status_code}"
        )
        if response.status_code == HTTPStatus.FORBIDDEN:
            return Err("Auth Failed")
        retry_count = 0
        while (
            response.status_code == HTTPStatus.TOO_MANY_REQUESTS
            and retry_count < max_retry_count
        ):
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


from marshmallow.exceptions import ValidationError

from dongtai_web.dongtai_sca.common.dataclass import (
    PackageInfo,
    PackageResponse,
    PackageVulResponse,
    Vul,
    VulInfo,
)


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
def get_package_vul(
    aql: str = "", ecosystem: str = "", package_hash: str = ""
) -> list[dict]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v1/package_vul/")
    querystring = (
        {"aql": aql} if aql else {"ecosystem": ecosystem, "hash": package_hash}
    )
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
def get_package_vul_v2(
    aql: str = "", ecosystem: str = "", package_hash: str = ""
) -> tuple[list[dict], list[dict]]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v2/package_vul/")
    querystring = (
        {"aql": aql} if aql else {"ecosystem": ecosystem, "hash": package_hash}
    )
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
def get_package_vul_v3(
    aql: str = "",
    ecosystem: str = "",
    package_version: str = "",
    package_name: str = "",
) -> tuple[tuple[Vul, ...], tuple[str, ...], tuple[str, ...]]:
    url = urljoin(
        SCA_BASE_URL,
        f"/openapi/sca/v3/package/{ecosystem.lower()}/{package_name}/{package_version}/vuls",
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
def get_package(
    aql: str = "", ecosystem: str = "", package_hash: str = ""
) -> list[dict]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v1/package/")
    querystring = (
        {"aql": aql} if aql else {"ecosystem": ecosystem, "hash": package_hash}
    )
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
def get_package_v2(
    aql: str = "", ecosystem: str = "", package_hash: str = ""
) -> list[dict]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v1/package/")
    querystring = (
        {"aql": aql} if aql else {"ecosystem": ecosystem, "hash": package_hash}
    )
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
def get_package_v3(
    aql: str = "", ecosystem: str = "", package_hash: str = ""
) -> list[PackageInfo]:
    url = urljoin(
        SCA_BASE_URL, f"/openapi/sca/v3/package/{ecosystem}/hash/{package_hash}"
    )
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
    while (
        res.is_err()
        and res.value == "Rate Limit Exceeded"
        and retry_count < SCA_MAX_RETRY_COUNT
    ):
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


LICENSE_DICT = {
    "GPL-1.0-only": {
        "id": 52,
        "identifier": "GPL-1.0-only",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-1.0-or-later": {
        "id": 53,
        "identifier": "GPL-1.0-or-later",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-only": {
        "id": 54,
        "identifier": "GPL-2.0-only",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-or-later": {
        "id": 55,
        "identifier": "GPL-2.0-or-later",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0-only": {
        "id": 56,
        "identifier": "GPL-3.0-only",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0-or-later": {
        "id": 57,
        "identifier": "GPL-3.0-or-later",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-1.0": {
        "id": 58,
        "identifier": "GPL-1.0",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-1.0+": {
        "id": 59,
        "identifier": "GPL-1.0+",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0": {
        "id": 60,
        "identifier": "GPL-2.0",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0+": {
        "id": 61,
        "identifier": "GPL-2.0+",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-autoconf-exception": {
        "id": 62,
        "identifier": "GPL-2.0-with-autoconf-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-bison-exception": {
        "id": 63,
        "identifier": "GPL-2.0-with-bison-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-classpath-exception": {
        "id": 64,
        "identifier": "GPL-2.0-with-classpath-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-font-exception": {
        "id": 65,
        "identifier": "GPL-2.0-with-font-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-2.0-with-GCC-exception": {
        "id": 66,
        "identifier": "GPL-2.0-with-GCC-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0": {
        "id": 67,
        "identifier": "GPL-3.0",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0+": {
        "id": 68,
        "identifier": "GPL-3.0+",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0-with-autoconf-exception": {
        "id": 69,
        "identifier": "GPL-3.0-with-autoconf-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "GPL-3.0-with-GCC-exception": {
        "id": 70,
        "identifier": "GPL-3.0-with-GCC-exception",
        "level_id": 1,
        "level_desc": "禁止商业闭源集成",
    },
    "AGPL-1.0-only": {
        "id": 71,
        "identifier": "AGPL-1.0-only",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-1.0-or-later": {
        "id": 72,
        "identifier": "AGPL-1.0-or-later",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-3.0-only": {
        "id": 73,
        "identifier": "AGPL-3.0-only",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-3.0-or-later": {
        "id": 74,
        "identifier": "AGPL-3.0-or-later",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-1.0": {
        "id": 75,
        "identifier": "AGPL-1.0",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "AGPL-3.0": {
        "id": 76,
        "identifier": "AGPL-3.0",
        "level_id": 1,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.0-only": {
        "id": 77,
        "identifier": "LGPL-2.0-only",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.0-or-later": {
        "id": 78,
        "identifier": "LGPL-2.0-or-later",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.1-only": {
        "id": 79,
        "identifier": "LGPL-2.1-only",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.1-or-later": {
        "id": 80,
        "identifier": "LGPL-2.1-or-later",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-3.0-only": {
        "id": 81,
        "identifier": "LGPL-3.0-only",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-3.0-or-later": {
        "id": 82,
        "identifier": "LGPL-3.0-or-later",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPLLR": {
        "id": 83,
        "identifier": "LGPLLR",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.0": {
        "id": 84,
        "identifier": "LGPL-2.0",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.0+": {
        "id": 85,
        "identifier": "LGPL-2.0+",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.1": {
        "id": 86,
        "identifier": "LGPL-2.1",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-2.1+": {
        "id": 87,
        "identifier": "LGPL-2.1+",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-3.0": {
        "id": 88,
        "identifier": "LGPL-3.0",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "LGPL-3.0+": {
        "id": 89,
        "identifier": "LGPL-3.0+",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "Artistic-1.0": {
        "id": 90,
        "identifier": "Artistic-1.0",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "Artistic-1.0-cl8": {
        "id": 91,
        "identifier": "Artistic-1.0-cl8",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "Artistic-1.0-Perl": {
        "id": 92,
        "identifier": "Artistic-1.0-Perl",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "Artistic-2.0": {
        "id": 93,
        "identifier": "Artistic-2.0",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "ClArtistic": {
        "id": 94,
        "identifier": "ClArtistic",
        "level_id": 2,
        "level_desc": "限制性商业闭源集成",
    },
    "ISC": {"id": 95, "identifier": "ISC", "level_id": 0, "level_desc": "允许商业集成"},
    "BSD-4-Clause": {
        "id": 96,
        "identifier": "BSD-4-Clause",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-2.5": {
        "id": 97,
        "identifier": "CC-BY-2.5",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-ND-4.0": {
        "id": 98,
        "identifier": "CC-BY-ND-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "BSD-2-Clause-Views": {
        "id": 99,
        "identifier": "BSD-2-Clause-Views",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "FTL": {"id": 100, "identifier": "FTL", "level_id": 0, "level_desc": "允许商业集成"},
    "BSD-2-Clause-Patent": {
        "id": 101,
        "identifier": "BSD-2-Clause-Patent",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "MPL-2.0-no-copyleft-exception": {
        "id": 102,
        "identifier": "MPL-2.0-no-copyleft-exception",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-3.0": {
        "id": 103,
        "identifier": "CC-BY-NC-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-ND-2.5": {
        "id": 104,
        "identifier": "CC-BY-NC-ND-2.5",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "GFDL-1.3": {
        "id": 105,
        "identifier": "GFDL-1.3",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "libpng-2.0": {
        "id": 106,
        "identifier": "libpng-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "AML": {"id": 107, "identifier": "AML", "level_id": 0, "level_desc": "允许商业集成"},
    "MIT": {"id": 108, "identifier": "MIT", "level_id": 0, "level_desc": "允许商业集成"},
    "CC-BY-SA-2.5": {
        "id": 109,
        "identifier": "CC-BY-SA-2.5",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "EPL-2.0": {
        "id": 110,
        "identifier": "EPL-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-SA-2.0": {
        "id": 111,
        "identifier": "CC-BY-SA-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Apache-2.0": {
        "id": 112,
        "identifier": "Apache-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "MPL-2.0": {
        "id": 113,
        "identifier": "MPL-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "BSD-3-Clause-Clear": {
        "id": 114,
        "identifier": "BSD-3-Clause-Clear",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-ND-3.0": {
        "id": 115,
        "identifier": "CC-BY-NC-ND-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-ND-4.0": {
        "id": 116,
        "identifier": "CC-BY-NC-ND-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-ND-3.0": {
        "id": 117,
        "identifier": "CC-BY-ND-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-2.5": {
        "id": 118,
        "identifier": "CC-BY-NC-2.5",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-SA-3.0": {
        "id": 119,
        "identifier": "CC-BY-SA-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "ECL-2.0": {
        "id": 120,
        "identifier": "ECL-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CDDL-1.0": {
        "id": 121,
        "identifier": "CDDL-1.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "MPL-1.1": {
        "id": 122,
        "identifier": "MPL-1.1",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC0-1.0": {
        "id": 123,
        "identifier": "CC0-1.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-4.0": {
        "id": 124,
        "identifier": "CC-BY-NC-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "JSON": {"id": 125, "identifier": "JSON", "level_id": 0, "level_desc": "允许商业集成"},
    "bzip2-1.0.6": {
        "id": 126,
        "identifier": "bzip2-1.0.6",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Apache-1.1": {
        "id": 127,
        "identifier": "Apache-1.1",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Beerware": {
        "id": 128,
        "identifier": "Beerware",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-2.0": {
        "id": 129,
        "identifier": "CC-BY-2.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-SA-3.0": {
        "id": 130,
        "identifier": "CC-BY-NC-SA-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "FSFAP": {"id": 131, "identifier": "FSFAP", "level_id": 0, "level_desc": "允许商业集成"},
    "CC-BY-3.0": {
        "id": 132,
        "identifier": "CC-BY-3.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-NC-SA-4.0": {
        "id": 133,
        "identifier": "CC-BY-NC-SA-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "CC-BY-4.0": {
        "id": 134,
        "identifier": "CC-BY-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "EPL-1.0": {
        "id": 135,
        "identifier": "EPL-1.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "UPL-1.0": {
        "id": 136,
        "identifier": "UPL-1.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Zlib": {"id": 137, "identifier": "Zlib", "level_id": 0, "level_desc": "允许商业集成"},
    "MIT-0": {"id": 138, "identifier": "MIT-0", "level_id": 0, "level_desc": "允许商业集成"},
    "CC-BY-SA-4.0": {
        "id": 139,
        "identifier": "CC-BY-SA-4.0",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "Unlicense": {
        "id": 140,
        "identifier": "Unlicense",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "HPND-sell-variant": {
        "id": 141,
        "identifier": "HPND-sell-variant",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "BSD-3-Clause": {
        "id": 142,
        "identifier": "BSD-3-Clause",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "BSD-2-Clause": {
        "id": 143,
        "identifier": "BSD-2-Clause",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
    "libtiff": {
        "id": 144,
        "identifier": "libtiff",
        "level_id": 0,
        "level_desc": "允许商业集成",
    },
}

LICENSE_ID_DICT = {v["id"]: k for k, v in LICENSE_DICT.items()}


def get_package_aql(name: str, ecosystem: str, version: str) -> str:
    return f"{ecosystem}:{name}:{version}"


def get_license_list(license_list_str: str) -> list[dict]:
    license_list = list(filter(lambda x: x, license_list_str.split(",")))
    res = list(
        PackageLicenseLevel.objects.filter(identifier__in=license_list)
        .values("identifier", "level_id", "level_desc")
        .all()
    )
    selected_identifier = [x["identifier"] for x in res]
    for k in license_list:
        if k not in selected_identifier:
            res.append({"identifier": k, "level_id": 0, "level_desc": "允许商业集成"})

    if res:
        return res
    return [{"identifier": "non-standard", "level_id": 0, "level_desc": "允许商业集成"}]


def get_license_list_v2(license_list: tuple[str, ...]) -> list[dict]:
    def filter_none(x: dict | None) -> bool:
        return x is not None

    return [
        LICENSE_DICT[license] for license in license_list if license in LICENSE_DICT
    ]
    # return [{


# temporary remove to fit in cython complier
def get_highest_license(license_list: list) -> dict:
    logger.debug(f"license_list : {license_list}")
    res = sorted(license_list, key=lambda x: x["level_id"], reverse=True)
    if res:
        return res[0]
    return {"identifier": "non-standard", "level_id": 0, "level_desc": "允许商业集成"}


def sha_1(raw):
    return sha1(raw.encode("utf-8"), usedforsecurity=False).hexdigest()


import contextlib
from dataclasses import asdict, dataclass


@dataclass
class PackageVulSummary:
    level: int = 0
    vul_count: int = 0
    vul_critical_count: int = 0
    vul_high_count: int = 0
    vul_medium_count: int = 0
    vul_low_count: int = 0
    vul_info_count: int = 0
    affected_versions: tuple[str, ...] = ()
    unaffected_versions: tuple[str, ...] = ()


def get_type_with_cwe(cwe_id: str) -> str:
    return ""


def sca_scan_asset_v2(
    aql: str, ecosystem: str, package_name: str, version: str
) -> PackageVulSummary:
    from dongtai_common.models.asset_vul_v2 import (
        IastAssetVulV2,
        IastVulAssetRelationV2,
    )

    vuls, affected_versions, unaffected_versions = get_package_vul_v3(
        ecosystem=ecosystem,
        package_version=version,
        package_name=package_name,
    )
    vul_asset_rel_list = []
    for vul in vuls:
        logger.debug(
            "vul_level %s", get_vul_level_dict()[vul.vul_info.severity.lower()]
        )
        IastAssetVulV2.objects.update_or_create(
            vul_id=vul.vul_info.vul_id,
            defaults={
                "vul_codes": vul.vul_codes.to_dict(),
                "vul_type": [
                    get_cwe_name(cwe) if get_cwe_name(cwe) else cwe
                    for cwe in vul.vul_info.cwe
                ],
                "vul_name": vul.vul_info.title,
                "vul_detail": vul.vul_info.description,
                "level": get_vul_level_dict()[vul.vul_info.severity.lower()],
                "references": [asdict(ref) for ref in vul.vul_info.references]
                if vul.vul_info.references
                else [],
                "update_time": vul.vul_info.update_time.timestamp(),
                "create_time": vul.vul_info.create_time.timestamp(),
                "change_time": vul.vul_info.change_time.timestamp(),
                "published_time": vul.vul_info.published_time.timestamp()
                if vul.vul_info.published_time
                else vul.vul_info.create_time.timestamp(),
                "affected_versions": vul.affected_versions,
                "unaffected_versions": vul.unaffected_versions,
            },
        )
        # need add update logic
        vul_asset_rel = IastVulAssetRelationV2(
            asset_vul_id=vul.vul_info.vul_id,
            asset_id=aql,
        )
        vul_asset_rel_list.append(vul_asset_rel)
    IastVulAssetRelationV2.objects.filter(asset_id=aql).delete()
    IastVulAssetRelationV2.objects.bulk_create(
        vul_asset_rel_list, ignore_conflicts=True
    )
    package_info_dict = stat_severity_v2([vul.vul_info for vul in vuls])
    logger.debug("package_info_dict: %s", package_info_dict)
    return PackageVulSummary(
        affected_versions=affected_versions,
        unaffected_versions=unaffected_versions,
        **package_info_dict,
    )


@shared_task(queue="dongtai-sca-task")
def new_update_one_sca(
    agent_id,
    package_path,
    package_signature,
    package_name,
    package_algorithm,
    package_version="",
):
    logger.info(
        f"SCA检测开始 [{agent_id} {package_path} {package_signature} {package_name} {package_algorithm} {package_version}]"
    )
    from dongtai_common.models.assetv2 import (
        AssetV2,
        AssetV2Global,
        IastAssetLicense,
        IastPackageGAInfo,
    )

    agent = IastAgent.objects.filter(id=agent_id).first()
    if not agent:
        logger.info(
            f"SCA检测找不到对应Agent [{agent_id} {package_path} {package_signature} {package_name} {package_algorithm} {package_version}]"
        )
        return
    if not package_signature:
        package_signature = sha_1(package_signature)
    if agent.language == "JAVA":
        packages = get_package_v3(ecosystem="maven", package_hash=package_signature)
    else:
        packages = get_package_v3(aql=package_name)
    asset_license_list = []
    for package in packages:
        aql = get_package_aql(package.name, package.ecosystem, package.version)
        license_list = get_license_list_v2(package.license)
        package_info = sca_scan_asset_v2(
            aql, package.ecosystem, package.name, package.version
        )
        obj, created = IastPackageGAInfo.objects.update_or_create(
            package_fullname=package.ecosystem + package.name,
            defaults={
                "affected_versions": package_info.affected_versions,
                "unaffected_versions": package_info.unaffected_versions,
            },
        )
        assetglobalobj, _ = AssetV2Global.objects.update_or_create(
            aql=aql,
            defaults={
                "signature_algorithm": "SHA-1",
                "language_id": get_language_id(
                    agent.language if agent.language else "JAVA"
                ),
                "package_fullname": obj,
                "package_name": package.name,
                "signature_value": package.hash,
                "version": package.version,
                "license_list": license_list,
            },
        )
        AssetV2.objects.update_or_create(
            aql=assetglobalobj,
            project_id=agent.bind_project_id,
            project_version_id=agent.project_version_id,
            defaults={
                "signature_algorithm": "SHA-1",
                "language_id": get_language_id(agent.language),
                "package_name": package.name,
                "package_path": package_path,
                "signature_value": package_signature,
                "version": package.version,
                "department_id": agent.bind_project.department_id,
            },
        )
        # need change package_name with ecosystem
        datadict = asdict(package_info)
        del datadict["affected_versions"]
        del datadict["unaffected_versions"]
        datadict["package_fullname"] = obj
        AssetV2Global.objects.filter(aql=aql).update(**datadict)
        for i in license_list:
            license = IastAssetLicense(license_id=i["id"], asset=assetglobalobj)
            asset_license_list.append(license)
    IastAssetLicense.objects.bulk_create(asset_license_list, ignore_conflicts=True)
    # create license list


@shared_task(queue="dongtai-sca-task")
def update_one_sca(
    agent_id,
    package_path,
    package_signature,
    package_name,
    package_algorithm,
    package_version="",
):
    logger.info(
        f"SCA检测开始 [{agent_id} {package_path} {package_signature} {package_name} {package_algorithm} {package_version}]"
    )
    agent = IastAgent.objects.filter(id=agent_id).first()
    if not package_signature:
        package_signature = sha_1(package_signature)
    if not SCA_SETUP:
        logger.warning("SCA_TOKEN not setup !")
        asset = Asset()
        new_level = IastVulLevel.objects.get(name="info")

        # change to update_or_create
        asset.package_name = package_name
        asset.package_path = package_path
        asset.signature_value = package_signature
        asset.signature_algorithm = "SHA-1"
        asset.version = package_version
        asset.level_id = new_level.id
        asset.vul_count = 0
        asset.language = agent.language
        if agent:
            asset.agent = agent
            asset.project_version_id = (
                agent.project_version_id if agent.project_version_id else 0
            )
            asset.project_name = agent.project_name
            asset.language = agent.language
            asset.project_id = -1
            if agent.bind_project_id:
                asset.project_id = agent.bind_project_id
                asset.department_id = agent.bind_project.department_id
            asset.user_id = -1
            if agent.user_id:
                asset.user_id = agent.user_id
        license_list = get_license_list("non-standard")
        asset.license_list = license_list
        highest_license = get_highest_license(license_list)
        asset.highest_license = get_highest_license(license_list)
        asset.license = highest_license["identifier"]
        asset.dt = int(time.time())
        asset.save()
        return

    if agent.language == "JAVA":
        packages = get_package(ecosystem="maven", package_hash=package_signature)
    else:
        packages = get_package(aql=package_name)
    if not packages:
        asset = Asset()
        new_level = IastVulLevel.objects.get(name="info")

        # change to update_or_create
        asset.package_name = package_name
        asset.package_path = package_path
        asset.signature_value = package_signature
        asset.signature_algorithm = "SHA-1"
        asset.version = package_version
        asset.level_id = new_level.id
        asset.vul_count = 0
        asset.language = agent.language
        if agent:
            asset.agent = agent
            asset.project_version_id = (
                agent.project_version_id if agent.project_version_id else 0
            )
            asset.project_name = agent.project_name
            asset.language = agent.language
            asset.project_id = -1
            if agent.bind_project_id:
                asset.project_id = agent.bind_project_id
                asset.department_id = agent.bind_project.department_id
            asset.user_id = -1
            if agent.user_id:
                asset.user_id = agent.user_id
        license_list = get_license_list("non-standard")
        asset.license_list = license_list
        highest_license = get_highest_license(license_list)
        asset.highest_license = get_highest_license(license_list)
        asset.license = highest_license["identifier"]
        asset.dt = int(time.time())
        asset.save()
        return

    for package in packages:
        asset = Asset()
        new_level = IastVulLevel.objects.get(name="info")
        aql = get_package_aql(package["name"], package["ecosystem"], package["version"])

        # change to update_or_create
        asset.package_name = aql
        asset.package_path = package_path
        asset.signature_value = package["hash"]
        asset.signature_algorithm = "SHA-1"
        asset.version = package["version"]
        asset.level_id = new_level.id
        asset.vul_count = 0
        asset.language = agent.language
        if agent:
            asset.agent = agent
            asset.project_version_id = (
                agent.project_version_id if agent.project_version_id else 0
            )
            asset.project_name = agent.project_name
            asset.language = agent.language
            asset.project_id = -1
            if agent.bind_project_id:
                asset.project_id = agent.bind_project_id
                asset.department_id = agent.bind_project.department_id
            asset.user_id = -1
            if agent.user_id:
                asset.user_id = agent.user_id
        license_list = get_license_list(
            package["license"] if package["license"] else "non-standard"
        )
        asset.license_list = license_list
        highest_license = get_highest_license(license_list)
        asset.highest_license = get_highest_license(license_list)
        asset.license = highest_license["identifier"]
        asset.dt = int(time.time())
        asset.save()
        sca_scan_asset(
            asset.id, package["ecosystem"], package["name"], package["version"]
        )


def stat_severity(serveritys: list) -> dict:
    dic = defaultdict(int)
    for serverity in serveritys:
        if serverity.lower() == "moderate":
            dic["critical"] += 1
        else:
            dic[serverity.lower()] += 1
    return dict(dic)


def stat_severity_v2(vul_infos: list[VulInfo]) -> dict:
    res = defaultdict(int)
    severitys = [x.severity for x in vul_infos]
    for serverity in severitys:
        if serverity.lower() == "moderate":
            res["medium"] += 1
        else:
            res[serverity.lower()] += 1

    for key in ("critical", "high", "medium", "low", "info"):
        if key not in res:
            res[key] = 0
    return dict(
        level=get_asset_level(dict(res)),
        vul_count=sum(res.values()),
        **{f"vul_{k}_count": v for k, v in res.items()},
    )


class DongTaiScaVersion(_BaseVersion):
    """
    Internal Temprorary Version Solution.
    Use to compare version.
    """

    def __init__(self, version: str) -> None:
        version_code = ""
        version_list = version.split(".")[0:4]
        while len(version_list) != 5:
            version_list.append("0")
        for _version in version_list:
            version_code += _version.zfill(5)
        self._key = (version_code,)
        self._version = version


def get_nearest_version(version_str: str, version_str_list: list[str]) -> str:
    return min(
        filter(
            lambda x: x >= DongTaiScaVersion(version_str),
            (DongTaiScaVersion(x) for x in version_str_list),
        ),
        default=DongTaiScaVersion(""),
    )._version


def get_latest_version(version_str_list: list[str]) -> str:
    return max(
        (DongTaiScaVersion(x) for x in version_str_list),
        default=DongTaiScaVersion(""),
    )._version


def get_cve_numbers(cve: str = "", cwe: list = [], cnvd: str = "", cnnvd: str = ""):
    return {"cve": cve, "cwe": cwe, "cnvd": cnvd, "cnnvd": cnnvd}


def get_vul_serial(
    title: str = "", cve: str = "", cwe: list = [], cnvd: str = "", cnnvd: str = ""
) -> str:
    return "|".join([title, cve, cnvd, cnnvd, *cwe])


def get_vul_level_dict() -> defaultdict:
    return defaultdict(
        lambda: 1, {"moderate": 2, "high": 3, "critical": 4, "medium": 2, "low": 1}
    )


def get_ecosystem_language_dict() -> defaultdict:
    return defaultdict(
        lambda: "JAVA",
        {"maven": "JAVA", "pypi": "PYTHON", "composer": "PHP", "golang": "GO"},
    )


def get_language(language_id: int) -> str:
    return defaultdict(
        lambda: "Java",
        {
            1: "Java",
            2: "Python",
            3: "PHP",
            4: "Golang",
        },
    )[language_id]


def get_language_id(language: str) -> int:
    return defaultdict(
        lambda: 1,
        {
            "java": 1,
            "python": 2,
            "php": 3,
            "golang": 4,
        },
    )[language.lower()]


def get_level(level_id: int) -> str:
    return defaultdict(
        lambda: "无风险",
        {
            1: "低危",
            2: "中危",
            3: "高危",
            4: "严重",
            0: "无风险",
        },
    )[level_id]


def get_license(license_id: int) -> str:
    return defaultdict(lambda: "non-standard", LICENSE_ID_DICT)[license_id]


def get_description(descriptions: list[dict]) -> str:
    if not descriptions:
        return ""
    return sorted(descriptions, key=lambda x: x["language"], reverse=True)[0]["content"]


def get_vul_path(base_aql: str, vul_package_path: list[dict] = []) -> list[str]:
    return [
        get_package_aql(x["name"], x["ecosystem"], x["version"])
        for x in vul_package_path
    ] + [base_aql]


def get_asset_level(res: dict) -> int:
    level_map = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    for k, v in level_map.items():
        if k in res and res[k] > 0:
            return v
    return 0


def get_detail(res: list[dict]) -> str:
    slice_first = sorted(res, key=lambda x: x["language"], reverse=True)[0:]
    if slice_first:
        return slice_first[0]["content"]
    return ""


def get_title(title_zh: str, title_en: str) -> str:
    title_list = list(filter(lambda x: x != "", [title_zh, title_en]))
    if title_list:
        return title_list[0]
    return ""


def sca_scan_asset(asset_id: int, ecosystem: str, package_name: str, version: str):
    aql = get_package_aql(package_name, ecosystem, version)
    package_vuls, safe_version = get_package_vul_v2(aql)
    res = stat_severity([x["severity"] for x in package_vuls])
    timestamp = int(time.time())
    package_language = get_ecosystem_language_dict()[ecosystem]
    Asset.objects.filter(pk=asset_id).update(level_id=get_asset_level(res))
    Asset.objects.filter(pk=asset_id).update(
        **{f"vul_{k}_count": v for k, v in res.items()}
    )
    Asset.objects.filter(pk=asset_id).update(vul_count=sum(res.values()))
    for vul in package_vuls:
        vul_dependency = get_vul_path(aql, vul["vul_package_path"])
        cve_numbers = get_cve_numbers(
            vul["cve"], vul["cwe_info"], vul["cnvd"], vul["cnnvd"]
        )
        nearest_fixed_version = get_nearest_version(
            version, [i["version"] for i in vul["fixed"]]
        )
        vul_serial = get_vul_serial(
            vul["vul_title"], vul["cve"], vul["cwe_info"], vul["cnvd"], vul["cnnvd"]
        )
        vul_level = get_vul_level_dict()[vul["severity"].lower()]
        detail = get_detail(vul["description"])
        # still need , save to asset_vul_relation
        # save to asset latest_version

        # where to place? save_version save to asset
        # effected save to asset_vul_relation
        package_effected_version_list = vul["effected"]
        package_fixed_version_list = vul["fixed"]

        # 兼容
        #
        if not IastAssetVul.objects.filter(sid=vul["sid"]).exists():
            asset_vul = (
                IastAssetVul.objects.filter(sid__isnull=True, cve_code=vul["cve"])
                .order_by("update_time")
                .first()
            )
            if asset_vul:
                asset_vul.sid = vul["sid"]
                asset_vul.save()
        asset_vul, _ = IastAssetVul.objects.update_or_create(
            sid=vul["sid"],
            defaults={
                "package_name": vul["name"],
                "level_id": vul_level,
                "vul_name": get_title(vul["vul_title"], vul["vul_title_en"]),
                "vul_detail": detail,
                "aql": aql,
                "package_version": version,
                "package_language": package_language,
                "have_article": 1 if vul["references"] else 0,
                "have_poc": 1 if vul["poc"] else 0,
                "vul_cve_nums": cve_numbers,
                "vul_serial": vul_serial,
                "vul_publish_time": vul["publish_time"],
                "vul_update_time": vul["vul_change_time"],
                "update_time": timestamp,
                "update_time_desc": -timestamp,
                "create_time": timestamp,
                "fix_plan": vul["fix_plan"],
                "poc": vul["poc"],
                "descriptions": vul["description"],
                "references": vul["references"],
            },
        )
        key: str = asset_vul.sid + aql
        with contextlib.suppress(IntegrityError):
            IastAssetVulRelationMetaData.objects.update_or_create(
                vul_asset_key=key,
                vul_dependency_path=vul_dependency,
                effected_version_list=package_effected_version_list,
                fixed_version_list=package_fixed_version_list,
                nearest_fixed_version=nearest_fixed_version,
            )

        asset_vul_relation, _ = IastVulAssetRelation.objects.update_or_create(
            asset_vul_id=asset_vul.id,
            asset_id=asset_id,
            defaults={
                "create_time": timestamp,
                "status_id": 1,
                "vul_asset_metadata_id": key,
            },
        )
        if len(vul["cwe_info"]) == 0:
            vul["cwe_info"].append("")
        for cwe_id in vul["cwe_info"]:
            if not IastAssetVulType.objects.filter(cwe_id=cwe_id).exists():
                try:
                    IastAssetVulType.objects.create(
                        cwe_id=cwe_id, name=get_cwe_name(cwe_id)
                    )
                except IntegrityError:
                    logger.debug("unique error stack: ", exc_info=True)
                    logger.info("unique error cause by concurrency insert,ignore it")
            type_ = IastAssetVulType.objects.filter(cwe_id=cwe_id).first()
            if not type_:
                logger.info("create type_ failed: %s", cwe_id)
                continue
            IastAssetVulTypeRelation.objects.get_or_create(
                asset_vul_id=asset_vul.id, asset_vul_type_id=type_.id
            )
    nearest_safe_version = get_nearest_version(
        version, [i["version"] for i in safe_version]
    )
    latest_safe_version = get_latest_version([i["version"] for i in safe_version])
    Asset.objects.filter(pk=asset_id).update(
        safe_version_list=safe_version,
        nearest_safe_version=nearest_safe_version,
        latest_safe_version=latest_safe_version,
    )
