from dongtai_common.models.asset_vul import IastAssetVulRelationMetaData
from django.db import IntegrityError
from .cwe import get_cwe_name
from dongtai_common.models.asset_vul import (IastAssetVulTypeRelation,
                                             IastAssetVul,
                                             IastVulAssetRelation,
                                             IastAssetVulType)
from packaging.version import _BaseVersion
from dongtai_common.models.asset_vul import IastAssetVul
from collections import defaultdict
from hashlib import sha1
from dongtai_conf.settings import SCA_SETUP
from dongtai_web.dongtai_sca.models import PackageLicenseLevel
from celery import shared_task
import time
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.models.asset import Asset
from dongtai_common.models.agent import IastAgent
import requests
from result import Ok, Err, Result
import logging
from requests.exceptions import ConnectionError, ConnectTimeout
from requests.exceptions import RequestException
import json
from json.decoder import JSONDecodeError
from typing import Optional, Callable, Any
from typing import List, Dict, Tuple
from requests import Response
from dongtai_conf.settings import SCA_BASE_URL, SCA_TIMEOUT
from urllib.parse import urljoin
from dongtai_common.common.utils import cached_decorator
from dongtai_common.models.profile import IastProfile
from json.decoder import JSONDecodeError
from http import HTTPStatus

logger = logging.getLogger("dongtai-webapi")


def get_sca_token() -> str:
    # profilefromdb = IastProfile.objects.filter(key='sca_token').values_list(
    #    'value', flat=True).first()
    # if profilefromdb:
    #    return profilefromdb
    # return ''
    from dongtai_conf.settings import SCA_TOKEN
    return SCA_TOKEN


def request_get_res_data_with_exception(
        data_extract_func: Callable[[Response], Result] = lambda x: Ok(x),
        *args,
        **kwargs) -> Result:
    try:
        response: Response = requests.request(*args, **kwargs)
        logger.debug(f"response content: {response.content!r}")
        logger.info(
            f"response content url: {response.url} status_code: {response.status_code}"
        )
        res = data_extract_func(response)
        if isinstance(res, Err):
            return res
        return Ok(res.value)
    except (ConnectionError, ConnectTimeout):
        return Err("ConnectionError with target server")
    except JSONDecodeError:
        logger.debug(f"content decode error :{response.content!r}")
        logger.info(f"content decode error")
        return Err("Content decode error")
    except RequestException as e:
        logger.error(e, exc_info=True)
        return Err("Request Exception")
    except Exception as e:
        logger.error(e, exc_info=True)
        return Err("Exception")


def data_transfrom(response: Response) -> Result[List[Dict], str]:
    if response.status_code == HTTPStatus.FORBIDDEN:
        return Err('Rate Limit Exceeded')
    try:
        res_data = json.loads(response.content)
        return Ok(res_data['data'])
    except JSONDecodeError as e:
        logger.debug(e, exc_info=True)
        logger.info(f'JSONDecodeError content: {response.content!r}')
        return Err('Failed')
    except KeyError as e:
        logger.debug(e, exc_info=True)
        logger.info(f'content form not match content: {response.content!r}')
        return Err('Failed')
    except Exception as e:
        logger.error(f"unexcepted Exception : {e}", exc_info=True)
        return Err('Failed')


def data_transfrom_package_vul_v2(
        response: Response) -> Result[List[Dict], str]:
    if response.status_code == HTTPStatus.FORBIDDEN:
        return Err('Rate Limit Exceeded')
    try:
        res_data = json.loads(response.content)
        return Ok((res_data['data'], res_data['safe_version']))
    except JSONDecodeError as e:
        logger.debug(e, exc_info=True)
        logger.info(f'JSONDecodeError content: {response.content!r}')
        return Err('Failed')
    except KeyError as e:
        logger.debug(e, exc_info=True)
        logger.info(f'content form not match content: {response.content!r}')
        return Err('Failed')
    except Exception as e:
        logger.error(f"unexcepted Exception : {e}", exc_info=True)
        return Err('Failed')


@cached_decorator(
    random_range=(2 * 60 * 60, 2 * 60 * 60), )
def get_package_vul(aql: str = "",
                    ecosystem: str = "",
                    package_hash: str = "") -> List[Dict]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v1/package_vul/")
    if aql:
        querystring = {"aql": aql}
    else:
        querystring = {"ecosystem": ecosystem, "hash": package_hash}
    headers = {"Token": get_sca_token()}
    payload = ""
    res = request_get_res_data_with_exception(data_transfrom,
                                              "GET",
                                              url,
                                              data=payload,
                                              params=querystring,
                                              headers=headers,
                                              timeout=SCA_TIMEOUT)
    if isinstance(res, Err):
        return []
    data = res.value
    return data


@cached_decorator(
    random_range=(2 * 60 * 60, 2 * 60 * 60), )
def get_package_vul_v2(
        aql: str = "",
        ecosystem: str = "",
        package_hash: str = "") -> Tuple[List[Dict], List[Dict]]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v2/package_vul/")
    if aql:
        querystring = {"aql": aql}
    else:
        querystring = {"ecosystem": ecosystem, "hash": package_hash}
    headers = {"Token": get_sca_token()}
    payload = ""
    res = request_get_res_data_with_exception(data_transfrom_package_vul_v2,
                                              "GET",
                                              url,
                                              data=payload,
                                              params=querystring,
                                              headers=headers,
                                              timeout=SCA_TIMEOUT)
    if isinstance(res, Err):
        return [], []
    data = res.value
    return data


@cached_decorator(
    random_range=(2 * 60 * 60, 2 * 60 * 60), )
def get_package(aql: str = "",
                ecosystem: str = "",
                package_hash: str = "") -> List[Dict]:
    url = urljoin(SCA_BASE_URL, "/openapi/sca/v1/package/")
    if aql:
        querystring = {"aql": aql}
    else:
        querystring = {"ecosystem": ecosystem, "hash": package_hash}
    headers = {"Token": get_sca_token()}
    payload = ""
    res = request_get_res_data_with_exception(data_transfrom,
                                              "GET",
                                              url,
                                              data=payload,
                                              params=querystring,
                                              headers=headers,
                                              timeout=SCA_TIMEOUT)
    if isinstance(res, Err):
        return []
    data = res.value
    return data


# from dongtai_web.dongtai_sca.utils import sca_scan_asset


def get_package_aql(name: str, ecosystem: str, version: str) -> str:
    return f"{ecosystem}:{name}:{version}"


def get_license_list(license_list_str: str) -> List[Dict]:
    license_list = list(filter(lambda x: x, license_list_str.split(",")))
    res = list(
        PackageLicenseLevel.objects.filter(identifier__in=license_list).values(
            'identifier', 'level_id', 'level_desc').all())
    selected_identifier = list(map(lambda x: x['identifier'], res))
    for k in license_list:
        if k not in selected_identifier:
            res.append({
                'identifier': k,
                "level_id": 0,
                "level_desc": "允许商业集成"
            })

    if res:
        return res
    return [{
        'identifier': "non-standard",
        "level_id": 0,
        "level_desc": "允许商业集成"
    }]


# temporary remove to fit in cython complier
def get_highest_license(license_list: list) -> dict:
    logger.debug(f'license_list : {license_list}')
    res = sorted(license_list, key=lambda x: x['level_id'], reverse=True)
    if res:
        return res[0]
    return {
        'identifier': "non-standard",
        "level_id": 0,
        "level_desc": "允许商业集成"
    }


def sha_1(raw):
    sha1_str = sha1(raw.encode("utf-8"), usedforsecurity=False).hexdigest()
    return sha1_str


@shared_task(queue='dongtai-sca-task')
def update_one_sca(agent_id,
                   package_path,
                   package_signature,
                   package_name,
                   package_algorithm,
                   package_version=''):
    logger.info(
        f'SCA检测开始 [{agent_id} {package_path} {package_signature} {package_name} {package_algorithm} {package_version}]'
    )
    agent = IastAgent.objects.filter(id=agent_id).first()
    if not package_signature:
        package_signature = sha_1(package_signature)
    if not SCA_SETUP:
        logger.warning(f"SCA_TOKEN not setup !")
        asset = Asset()
        new_level = IastVulLevel.objects.get(name="info")

        # change to update_or_create
        asset.package_name = package_name
        asset.package_path = package_path
        asset.signature_value = package_signature
        asset.signature_algorithm = 'SHA-1'
        asset.version = package_version
        asset.level_id = new_level.id
        asset.vul_count = 0
        asset.language = agent.language
        if agent:
            asset.agent = agent
            asset.project_version_id = agent.project_version_id if agent.project_version_id else 0
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
        asset.license = highest_license['identifier']
        asset.dt = int(time.time())
        asset.save()
        return

    if agent.language == "JAVA":
        packages = get_package(ecosystem='maven',
                               package_hash=package_signature)
    else:
        packages = get_package(aql=package_name)
    if not packages:
        asset = Asset()
        new_level = IastVulLevel.objects.get(name="info")

        # change to update_or_create
        asset.package_name = package_name
        asset.package_path = package_path
        asset.signature_value = package_signature
        asset.signature_algorithm = 'SHA-1'
        asset.version = package_version
        asset.level_id = new_level.id
        asset.vul_count = 0
        asset.language = agent.language
        if agent:
            asset.agent = agent
            asset.project_version_id = agent.project_version_id if agent.project_version_id else 0
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
        asset.license = highest_license['identifier']
        asset.dt = int(time.time())
        asset.save()
        return

    for package in packages:
        asset = Asset()
        new_level = IastVulLevel.objects.get(name="info")
        aql = get_package_aql(package['name'], package['ecosystem'],
                              package['version'])

        # change to update_or_create
        asset.package_name = aql
        asset.package_path = package_path
        asset.signature_value = package['hash']
        asset.signature_algorithm = 'SHA-1'
        asset.version = package['version']
        asset.level_id = new_level.id
        asset.vul_count = 0
        asset.language = agent.language
        if agent:
            asset.agent = agent
            asset.project_version_id = agent.project_version_id if agent.project_version_id else 0
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
            package['license'] if package['license'] else "non-standard")
        asset.license_list = license_list
        highest_license = get_highest_license(license_list)
        asset.highest_license = get_highest_license(license_list)
        asset.license = highest_license['identifier']
        asset.dt = int(time.time())
        asset.save()
        sca_scan_asset(asset.id, package['ecosystem'], package['name'],
                       package['version'])


def stat_severity(serveritys: list) -> dict:
    dic = defaultdict(int)
    for serverity in serveritys:
        if serverity.lower() == 'moderate':
            dic['critical'] += 1
        else:
            dic[serverity.lower()] += 1
    return dict(dic)


class DongTaiScaVersion(_BaseVersion):
    """
    Internal Temprorary Version Solution.
    Use to compare version.
    """

    def __init__(self, version: str) -> None:
        version_code = ""
        version_list = version.split('.')[0:4]
        while len(version_list) != 5:
            version_list.append("0")
        for _version in version_list:
            version_code += _version.zfill(5)
        self._key = version_code
        self._version = version


def get_nearest_version(version_str: str, version_str_list: List[str]) -> str:
    return min(filter(lambda x: x >= DongTaiScaVersion(version_str),
                      map(lambda x: DongTaiScaVersion(x), version_str_list)),
               default=DongTaiScaVersion(""))._version


def get_latest_version(version_str_list: List[str]) -> str:
    return max(map(lambda x: DongTaiScaVersion(x), version_str_list),
               default=DongTaiScaVersion(""))._version


def get_cve_numbers(cve: str = "",
                    cwe: list = [],
                    cnvd: str = "",
                    cnnvd: str = ""):
    return {'cve': cve, 'cwe': cwe, 'cnvd': cnvd, 'cnnvd': cnnvd}


def get_vul_serial(title: str = "",
                   cve: str = "",
                   cwe: list = [],
                   cnvd: str = "",
                   cnnvd: str = "") -> str:
    return "|".join([title, cve, cnvd, cnnvd] + cwe)


def get_vul_level_dict() -> defaultdict:
    return defaultdict(lambda: 5, {
        'moderate': 1,
        'high': 1,
        "critical": 1,
        "medium": 2,
        "low": 3
    })


def get_ecosystem_language_dict() -> defaultdict:
    return defaultdict(lambda: 'JAVA', {
        'maven': 'JAVA',
        "pypi": 'PYTHON',
        "composer": 'PHP',
        "golang": 'GO'
    })


def get_description(descriptions: List[Dict]) -> str:
    if not descriptions:
        return ""
    return sorted(descriptions, key=lambda x: x['language'],
                  reverse=True)[0]['content']


def get_vul_path(base_aql: str,
                 vul_package_path: List[Dict] = []) -> List[str]:
    return list(
        map(lambda x: get_package_aql(x['name'], x['ecosystem'], x['version']),
            vul_package_path)) + [base_aql]


def get_asset_level(res: dict) -> int:
    level_map = {
        'critical': 1,
        'high': 1,
        'medium': 2,
        'low': 3
    }
    for k, v in level_map.items():
        if k in res and res[k] > 0:
            return v
    return 4


def get_detail(res: List[Dict]) -> str:
    slice_first = sorted(res, key=lambda x: x['language'], reverse=True)[0:]
    if slice_first:
        return slice_first[0]["content"]
    return ""


def get_title(title_zh: str, title_en: str) -> str:
    title_list = list(filter(lambda x: x != "", [title_zh, title_en]))
    if title_list:
        return title_list[0]
    return ""


def sca_scan_asset(asset_id: int, ecosystem: str, package_name: str,
                   version: str):
    aql = get_package_aql(package_name, ecosystem, version)
    package_vuls, safe_version = get_package_vul_v2(aql)
    res = stat_severity(list(map(lambda x: x["severity"], package_vuls)))
    timestamp = int(time.time())
    package_language = get_ecosystem_language_dict()[ecosystem]
    Asset.objects.filter(pk=asset_id).update(level_id=get_asset_level(res))
    Asset.objects.filter(pk=asset_id).update(
        **{f"vul_{k}_count": v
           for k, v in res.items()})
    Asset.objects.filter(pk=asset_id).update(
        **{"vul_count": sum(res.values())})
    for vul in package_vuls:
        vul_dependency = get_vul_path(aql, vul['vul_package_path'])
        cve_numbers = get_cve_numbers(vul['cve'], vul['cwe_info'], vul['cnvd'],
                                      vul['cnnvd'])
        nearest_fixed_version = get_nearest_version(
            version, [i['version'] for i in vul['fixed']])
        vul_serial = get_vul_serial(vul['vul_title'], vul['cve'],
                                    vul['cwe_info'], vul['cnvd'], vul['cnnvd'])
        vul_level = get_vul_level_dict()[vul['severity'].lower()]
        detail = get_detail(vul['description'])
        # still need , save to asset_vul_relation
        # nearest_fixed_version = get_nearest_version(version, vul['fixed'])
        # save to asset latest_version
        # latest_version = get_latest_version(vul['safe_version'])

        # where to place? save_version save to asset
        # package_safe_version_list = vul['safe_version']
        # effected save to asset_vul_relation
        package_effected_version_list = vul['effected']
        package_fixed_version_list = vul['fixed']

        # 兼容
        #
        if not IastAssetVul.objects.filter(sid=vul['sid']).exists():
            asset_vul = IastAssetVul.objects.filter(
                sid__isnull=True,
                cve_code=vul['cve']).order_by('update_time').first()
            if asset_vul:
                asset_vul.sid = vul['sid']
                asset_vul.save()
        asset_vul, _ = IastAssetVul.objects.update_or_create(
            sid=vul['sid'],
            defaults={
                "package_name": vul['name'],
                "level_id": vul_level,
                "vul_name": get_title(vul['vul_title'], vul['vul_title_en']),
                "vul_detail": detail,
                "aql": aql,
                # package_hash=vul_package_hash, #???
                "package_version": version,
                # package_latest_version=latest_version,
                "package_language": package_language,
                "have_article": 1 if vul['references'] else 0,
                "have_poc": 1 if vul['poc'] else 0,
                # cve_id=cve_relation.id,
                "vul_cve_nums": cve_numbers,
                "vul_serial": vul_serial,
                "vul_publish_time": vul['publish_time'],
                "vul_update_time": vul['vul_change_time'],
                "update_time": timestamp,
                "update_time_desc": -timestamp,
                "create_time": timestamp,
                "fix_plan": vul['fix_plan'],
                "poc": vul['poc'],
                "descriptions": vul['description'],
                "references": vul['references'],
            },
        )
        key: str = asset_vul.sid + aql
        try:
            IastAssetVulRelationMetaData.objects.update_or_create(
                vul_asset_key=key,
                **{
                    "vul_dependency_path": vul_dependency,
                    "effected_version_list": package_effected_version_list,
                    "fixed_version_list": package_fixed_version_list,
                    "nearest_fixed_version": nearest_fixed_version,
                })
        except IntegrityError as e:
            pass
        asset_vul_relation, _ = IastVulAssetRelation.objects.update_or_create(
            asset_vul_id=asset_vul.id,
            asset_id=asset_id,
            defaults={
                "create_time": timestamp,
                "status_id": 1,
                "vul_asset_metadata_id": key,
            },
        )
        if len(vul['cwe_info']) == 0:
            vul['cwe_info'].append('')
        for cwe_id in vul['cwe_info']:
            if not IastAssetVulType.objects.filter(cwe_id=cwe_id).exists():
                try:
                    IastAssetVulType.objects.create(cwe_id=cwe_id,
                                                    name=get_cwe_name(cwe_id))
                except IntegrityError as e:
                    logger.debug("unique error stack: ", exc_info=True)
                    logger.info(
                        "unique error cause by concurrency insert,ignore it")
            type_: IastAssetVulType = IastAssetVulType.objects.filter(
                cwe_id=cwe_id).first()
            IastAssetVulTypeRelation.objects.get_or_create(
                asset_vul_id=asset_vul.id, asset_vul_type_id=type_.id)
    nearest_safe_version = get_nearest_version(
        version, [i['version'] for i in safe_version])
    latest_safe_version = get_latest_version(
        [i['version'] for i in safe_version])
    Asset.objects.filter(pk=asset_id).update(
        safe_version_list=safe_version,
        nearest_safe_version=nearest_safe_version,
        latest_safe_version=latest_safe_version)
