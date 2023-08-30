import contextlib
import logging
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from hashlib import sha1

from celery import shared_task
from django.db import IntegrityError
from django.db.models import Q

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.asset import Asset
from dongtai_common.models.asset_vul import (
    IastAssetVul,
    IastAssetVulRelationMetaData,
    IastAssetVulType,
    IastAssetVulTypeRelation,
    IastVulAssetRelation,
    IastVulLevel,
)
from dongtai_common.models.package_focus import IastPackageFocus
from dongtai_conf.settings import SCA_SETUP
from dongtai_protocol.views.hook_profiles import LANGUAGE_DICT
from dongtai_web.dongtai_sca.common.dataclass import VulInfo

from .cwe import get_cwe_name
from .requrest import (
    get_package,
    get_package_v3,
    get_package_vul_v2,
    get_package_vul_v4,
)
from .utils import (
    get_asset_level,
    get_cve_numbers,
    get_detail,
    get_ecosystem_language_dict,
    get_highest_license,
    get_language_id,
    get_latest_version,
    get_license_list,
    get_license_list_v2,
    get_nearest_version,
    get_package_aql,
    get_title,
    get_vul_level_dict,
    get_vul_path,
    get_vul_serial,
)

logger = logging.getLogger("dongtai-webapi")


def sha_1(raw):
    return sha1(raw.encode("utf-8"), usedforsecurity=False).hexdigest()


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


def sca_scan_asset_v2(aql: str, ecosystem: str, package_name: str, version: str) -> PackageVulSummary:
    from dongtai_common.models.asset_vul_v2 import IastAssetVulV2, IastVulAssetRelationV2

    vuls, affected_versions, unaffected_versions = get_package_vul_v4(
        ecosystem=ecosystem,
        package_version=version,
        package_name=package_name,
    )
    vul_asset_rel_list = []
    for vul in vuls:
        logger.debug("vul_level %s", get_vul_level_dict()[vul.vul_info.severity.lower()])
        IastAssetVulV2.objects.update_or_create(
            vul_id=vul.vul_info.vul_id,
            defaults={
                "vul_codes": vul.vul_codes.to_dict(),
                "vul_type": [get_cwe_name(cwe) if get_cwe_name(cwe) else cwe for cwe in vul.vul_info.cwe],
                "vul_name": vul.vul_info.title.en,
                "vul_name_zh": vul.vul_info.title.zh,
                "vul_detail": vul.vul_info.description.en,
                "vul_detail_zh": vul.vul_info.description.zh,
                "level": get_vul_level_dict()[vul.vul_info.severity.lower()],
                "references": [asdict(ref) for ref in vul.vul_info.references] if vul.vul_info.references else [],
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
    IastVulAssetRelationV2.objects.bulk_create(vul_asset_rel_list, ignore_conflicts=True)
    package_info_dict = stat_severity_v2([vul.vul_info for vul in vuls])
    logger.debug("package_info_dict: %s", package_info_dict)
    return PackageVulSummary(
        affected_versions=affected_versions,
        unaffected_versions=unaffected_versions,
        **package_info_dict,
    )


def sca_scan_asset(asset_id: int, ecosystem: str, package_name: str, version: str):
    aql = get_package_aql(package_name, ecosystem, version)
    package_vuls, safe_version = get_package_vul_v2(aql)
    res = stat_severity([x["severity"] for x in package_vuls])
    timestamp = int(time.time())
    package_language = get_ecosystem_language_dict()[ecosystem]
    Asset.objects.filter(pk=asset_id).update(level_id=get_asset_level(res))
    Asset.objects.filter(pk=asset_id).update(**{f"vul_{k}_count": v for k, v in res.items()})
    Asset.objects.filter(pk=asset_id).update(vul_count=sum(res.values()))
    for vul in package_vuls:
        vul_dependency = get_vul_path(aql, vul["vul_package_path"])
        cve_numbers = get_cve_numbers(vul["cve"], vul["cwe_info"], vul["cnvd"], vul["cnnvd"])
        nearest_fixed_version = get_nearest_version(version, [i["version"] for i in vul["fixed"]])
        vul_serial = get_vul_serial(vul["vul_title"], vul["cve"], vul["cwe_info"], vul["cnvd"], vul["cnnvd"])
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
                IastAssetVul.objects.filter(sid__isnull=True, cve_code=vul["cve"]).order_by("update_time").first()
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
                    IastAssetVulType.objects.create(cwe_id=cwe_id, name=get_cwe_name(cwe_id))
                except IntegrityError:
                    logger.debug("unique error stack: ", exc_info=True)
                    logger.info("unique error cause by concurrency insert,ignore it")
            type_ = IastAssetVulType.objects.filter(cwe_id=cwe_id).first()
            if not type_:
                logger.info("create type_ failed: %s", cwe_id)
                continue
            IastAssetVulTypeRelation.objects.get_or_create(asset_vul_id=asset_vul.id, asset_vul_type_id=type_.id)
    nearest_safe_version = get_nearest_version(version, [i["version"] for i in safe_version])
    latest_safe_version = get_latest_version([i["version"] for i in safe_version])
    Asset.objects.filter(pk=asset_id).update(
        safe_version_list=safe_version,
        nearest_safe_version=nearest_safe_version,
        latest_safe_version=latest_safe_version,
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
    is_focus = IastPackageFocus.objects.filter(
        Q(package_version=package_version) | Q(package_name=package_name, package_version=""),
        language_id=LANGUAGE_DICT.get(agent.language, None),
        package_name=package_name,
    ).exists()
    for package in packages:
        aql = get_package_aql(package.name, package.ecosystem, package.version)
        license_list = get_license_list_v2(package.license)
        package_info = sca_scan_asset_v2(aql, package.ecosystem, package.name, package.version)
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
                "language_id": get_language_id(agent.language if agent.language else "JAVA"),
                "package_fullname": obj,
                "package_name": package.name,
                "signature_value": package.hash,
                "version": package.version,
                "license_list": license_list,
                "is_focus": is_focus,
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
        license_list = get_license_list(package["license"] if package["license"] else "non-standard")
        asset.license_list = license_list
        highest_license = get_highest_license(license_list)
        asset.highest_license = get_highest_license(license_list)
        asset.license = highest_license["identifier"]
        asset.dt = int(time.time())
        asset.save()
        sca_scan_asset(asset.id, package["ecosystem"], package["name"], package["version"])
