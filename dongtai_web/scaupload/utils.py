######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : utils
# @created     : 星期六 1月 15, 2022 03:04:03 CST
#
# @description :
######################################################################


class ScaLibError(Exception):
    pass


def get_packge_from_sca_lib(**kwargs):
    return get_from_sca_lib("/package/", **kwargs)


def get_packge_vul_from_sca_lib(**kwargs):
    return get_from_sca_lib("/package_vul/", **kwargs)


def get_from_sca_lib(url, **kwargs):
    import json
    from urllib.parse import urljoin

    import requests

    from dongtai_conf.settings import SCA_BASE_URL

    finalurl = urljoin(SCA_BASE_URL, url)
    try:
        resp = requests.get(url=finalurl, params=kwargs)
        if resp.status_code == 200:
            json = json.loads(resp.content.decode())
    except Exception:
        raise ScaLibError("read from sca lib failure")
    return json
