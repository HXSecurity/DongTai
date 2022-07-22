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
        sca_scan_asset(asset.id, aql)

from collections import defaultdict
from dongtai_common.models.asset_vul import IastAssetVul


def stat_severity(serveritys):
    dic = defaultdict(int)
    for serverity in serveritys:
        if serverity not in dic:
            dic[serverity] = 1
        else:
            dic[serverity] += 1
    return dic

#from dongtai_common.models.asset import Asset
#def sca_scan_asset(asset_id: int, aql: str):
#    package_vuls = get_package_vul(aql)
#    res = stat_severity(map(lambda x: x["severity"], package_vuls))
#    for vul in package_vuls:
#        aql = get_package_aql(vul['name'], vul['ecosystem'], vul['version'])
#        asset_vul = IastAssetVul.objects.create(
#            package_name=vul['name'],
#            level_id=vul_level,
#            #license=vul_license, #???
#            #license_level=vul_license_level, #???
#            vul_name=vul['vul_title'],
#            vul_detail=vul['description'],
#            aql=aql,
#            # package_hash=vul_package_hash, #???
#            package_version=vul_package_v,
#            package_safe_version=vul_package_safe_version,
#            package_latest_version=vul_package_latest_version,
#            package_language=vul_package_language,
#            have_article=vul_have_article,
#            have_poc=vul_have_poc,
#            cve_id=cve_relation.id,
#            cve_code=cve_relation.cve,
#            vul_cve_nums=vul_reference,
#            vul_serial=vul_serial,
#            vul_publish_time=cve_relation.publish_time,
#            vul_update_time=cve_relation.update_time,
#            update_time=timestamp,
#            update_time_desc=-timestamp,
#            create_time=timestamp)
#        pass
#        #print(vul)
