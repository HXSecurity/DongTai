import requests
from result import Ok, Err, Result
import logging
from requests.exceptions import ConnectionError, ConnectTimeout
from requests.exceptions import RequestException
logger = logging.getLogger("dongtai-webapi")
import json
from json.decoder import JSONDecodeError
from typing import Optional, Callable, Any
from typing import List, Dict, Tuple
from requests import Response


def request_get_res_data_with_exception(data_extract_func: Callable[
    [Response], Any] = lambda x: x,
                                        *args,
                                        **kwargs) -> Result:
    try:
        response = requests.request(*args, **kwargs)
        logger.debug(f"response content: {response.content}")
        logger.debug(f"response content status_code: {response.status_code}")
        return Ok(data_extract_func(response))
    except (ConnectionError, ConnectTimeout):
        return Err("ConnectionError with target server")
    except JSONDecodeError:
        logger.debug(f"content decode error :{response.content}")
        logger.info(f"content decode error")
        return Err("Content decode error")
    except RequestException as e:
        logger.error(e, exc_info=True)
        return Err("Request Exception")
    except Exception as e:
        logger.error(e, exc_info=True)
        return Err("Exception")


def data_transfrom(response: Response) -> Tuple[int, Any]:
    res_data = json.loads(response.content)
    return [response.status_code, res_data]


def get_package_vul(aql: Optional[str] = None,
                    ecosystem: Optional[str] = None,
                    package_hash: Optional[str] = None) -> List[Dict]:
    url = "http://192.168.0.64:8283/openapi/sca/v1/package_vul/"
    if aql is not None:
        querystring = {"aql": aql}
    else:
        querystring = {"ecosystem": ecosystem, "hash": package_hash}

    payload = ""
    response = request_get_res_data_with_exception(data_transfrom,
                                                   "GET",
                                                   url,
                                                   data=payload,
                                                   params=querystring)
    if isinstance(response, Err):
        return []
    _ , data = response.value
    return data['data']

def get_package(aql: Optional[str] = None,
                ecosystem: Optional[str] = None,
                package_hash: Optional[str] = None) -> List[Dict]:
    url = "http://192.168.0.64:8283/openapi/sca/v1/package/"
    if aql is not None:
        querystring = {"aql": aql}
    else:
        querystring = {"ecosystem": ecosystem, "hash": package_hash}

    payload = ""
    response = request_get_res_data_with_exception(data_transfrom,
                                                   "GET",
                                                   url,
                                                   data=payload,
                                                   params=querystring)
    if isinstance(response, Err):
        return []
    _, data = response.value
    return data['data']

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.asset import Asset
from dongtai_common.models.vul_level import IastVulLevel
import time
#from dongtai_web.dongtai_sca.utils import sca_scan_asset

def get_package_aql(name: str, ecosystem: str, version: str) -> str:
    return f"{ecosystem}:{name}:{version}"


def update_one_sca(agent_id,
                   package_path,
                   package_signature,
                   package_name,
                   package_algorithm,
                   package_version=''):
    agent = IastAgent.objects.filter(id=agent_id).first()
    if agent.language == "JAVA":
        packages = get_package(ecosystem='maven',
                              package_hash=package_signature)
    else:
        packages = get_package_vul(aql=package_name)
    for package in packages:
        asset = Asset()
        new_level = IastVulLevel.objects.get(name="info")
        aql = get_package_aql(package['name'],
                                             package['ecosystem'],
                                             package['version'])
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
            asset.user_id = -1
            if agent.user_id:
                asset.user_id = agent.user_id

        asset.license = ''
        asset.dt = int(time.time())
        asset.save()
        sca_scan_asset(asset.id, package['ecosystem'], package['name'],
                       package['version'])

from collections import defaultdict
from dongtai_common.models.asset_vul import IastAssetVul


def stat_severity(serveritys) -> defaultdict:
    dic = defaultdict(int)
    for serverity in serveritys:
        dic[serverity] += 1
    return dic

from dongtai_common.models.asset import Asset
from packaging.version import Version, parse


def get_nearest_version(version_str: str, version_str_list: List[str]) -> str:
    return min(filter(lambda x: x > parse(version_str), map(parse,
                                                            version_str_list)))._version


def get_latest_version(version_str_list: List[str]) -> str:
    return max(map(parse, version_str_list))._version

def get_cve_numbers(cve: Optional[str] = "",
                    cwe: Optional[list] = [],
                    cnvd: Optional[str] = "",
                    cnnvd: Optional[str] = ""):
    return {'cve': cve, 'cwe': cwe, 'cnvd': cnvd, 'cnnvd': cnnvd}


def get_vul_serial(title: Optional[str] = "",
                   cve: Optional[str] = "",
                   cwe: Optional[list] = [],
                   cnvd: Optional[str] = "",
                   cnnvd: Optional[str] = "") -> str:
    return "|".join([title, cve, cnvd, cnnvd] + cwe)


from collections import defaultdict


def get_vul_level_dict() -> defaultdict:
    return defaultdict(lambda: 5, {
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


from dongtai_common.models.asset_vul import IastAssetVul, IastVulAssetRelation, IastAssetVulType

def sca_scan_asset(asset_id: int, ecosystem: str, package_name: str,
                   version: str):
    aql = get_package_aql(package_name, ecosystem, version)
    package_vuls = get_package_vul(aql)
    res = stat_severity(map(lambda x: x["severity"], package_vuls))
    timestamp = int(time.time())
    package_language = get_ecosystem_language_dict()[ecosystem]
    Asset.objects.filter(pk=asset_id).update(
        **{f"vul_{k}_count": v
           for k, v in res.items()})
    Asset.objects.filter(pk=asset_id).update(
        **{"vul_count": sum(res.values())})
    for vul in package_vuls:
        vul_dependency = get_vul_path(aql, vul['vul_package_path'])
        cve_numbers = get_cve_numbers(vul['cve'], vul['cwe_info'], vul['cnvd'],
                                      vul['cnnvd'])
        safe_version = get_nearest_version(version, vul['safe_version'])
        vul_serial = get_vul_serial(vul['vul_title'], vul['cve'],
                                    vul['cwe_info'], vul['cnvd'], vul['cnnvd'])
        vul_level = get_vul_level_dict()[vul['severity']]

        #still need?
        #fix_version = get_nearest_version(version, vul['fixed'])
        #latest_version = get_latest_version(vul['safe_version'])

        # where to place?
        #package_safe_version_list=vul['safe_version'],
        #package_effected_version_list=vul['effected']
        #package_fixed_version_list=vul['fixed']
        asset_vul = IastAssetVul.objects.create(
            package_name=vul['name'],
            level_id=vul_level,
            vul_name=vul['vul_title'],
            vul_detail=vul['description'],
            aql=aql,
            # package_hash=vul_package_hash, #???
            package_version=version,
            package_safe_version=safe_version,
            #package_latest_version=latest_version,
            package_language=package_language,
            have_article=1 if vul['references'] else 0,
            have_poc=1 if vul['poc'] else 0,
            #cve_id=cve_relation.id,
            cve_code=vul['cve'],
            vul_cve_nums=cve_numbers,
            vul_serial=vul_serial,
            vul_publish_time=vul['publish_time'],
            vul_update_time=vul['vul_change_time'],
            update_time=timestamp,
            update_time_desc=-timestamp,
            create_time=timestamp)
        asset_vul_relation = IastVulAssetRelation.objects.create(
            asset_vul_id=asset_vul.id,
            asset_id=asset_id,
            create_time=timestamp,
            vul_dependency_path=vul_dependency,
            status_id=1)
