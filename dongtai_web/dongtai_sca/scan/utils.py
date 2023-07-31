import json
import logging
from collections import defaultdict

from packaging.version import _BaseVersion

from dongtai_common.models.profile import IastProfile
from dongtai_web.dongtai_sca.models import PackageLicenseLevel

from .cwe import LICENSE_DICT, LICENSE_ID_DICT

logger = logging.getLogger("dongtai-webapi")


def get_sca_token() -> str:
    from dongtai_conf.settings import SCA_TOKEN

    return SCA_TOKEN


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
    res.extend(
        {"identifier": k, "level_id": 0, "level_desc": "允许商业集成"} for k in license_list if k not in selected_identifier
    )

    if res:
        return res
    return [{"identifier": "non-standard", "level_id": 0, "level_desc": "允许商业集成"}]


def get_license_list_v2(license_list: tuple[str, ...]) -> list[dict]:
    return [LICENSE_DICT[license] for license in license_list if license in LICENSE_DICT]
    # return [{


# temporary remove to fit in cython complier
def get_highest_license(license_list: list) -> dict:
    logger.debug(f"license_list : {license_list}")
    res = sorted(license_list, key=lambda x: x["level_id"], reverse=True)
    if res:
        return res[0]
    return {"identifier": "non-standard", "level_id": 0, "level_desc": "允许商业集成"}


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


def get_cve_numbers(cve: str = "", cwe: list | None = None, cnvd: str = "", cnnvd: str = ""):
    if cwe is None:
        cwe = []
    return {"cve": cve, "cwe": cwe, "cnvd": cnvd, "cnnvd": cnnvd}


def get_vul_serial(
    title: str = "",
    cve: str = "",
    cwe: list | None = None,
    cnvd: str = "",
    cnnvd: str = "",
) -> str:
    if cwe is None:
        cwe = []
    return "|".join([title, cve, cnvd, cnnvd, *cwe])


def get_vul_level_dict() -> defaultdict:
    return defaultdict(lambda: 1, {"moderate": 2, "high": 3, "critical": 4, "medium": 2, "low": 1})


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


def get_vul_path(base_aql: str, vul_package_path: list[dict] | None = None) -> list[str]:
    if vul_package_path is None:
        vul_package_path = []
    return [
        *[get_package_aql(x["name"], x["ecosystem"], x["version"]) for x in vul_package_path],
        base_aql,
    ]


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


PROFILE_KEY = "sca_language"
DEFAULT_SCA_LANGUAGE = {"language": "en"}


def get_sca_language_profile() -> dict[str, str]:
    profile = IastProfile.objects.filter(key=PROFILE_KEY).values_list("value", flat=True).first()
    if profile is None:
        IastProfile(
            key=PROFILE_KEY,
            value=json.dumps(PROFILE_KEY),
        ).save()
        return DEFAULT_SCA_LANGUAGE
    return json.loads(profile)
