from celery import shared_task
from celery.apps.worker import logger

from dongtai_common.models.asset import Asset, IastAssetDocument
from dongtai_common.models.asset_vul import (
    IastAssetVulnerabilityDocument,
    IastVulAssetRelation,
)
from dongtai_common.models.vulnerablity import (
    IastVulnerabilityDocument,
    IastVulnerabilityModel,
)


@shared_task
def data_correction_interpetor(situation: str):
    logger.info(f"data incorrect detected, situation {situation} is handling")
    if situation == "project_missing":
        data_correction_project(-1)
    elif situation == "vulnerablity_sync_fail":
        data_correction_all()


def data_correction_project(project_id):
    qs = IastVulnerabilityModel.objects.filter(agent__bind_project_id=project_id).all()
    IastVulnerabilityDocument().update(list(qs))
    qs = Asset.objects.filter(agent__bind_project_id=project_id).all()
    IastAssetDocument().update(list(qs))
    qs = IastVulAssetRelation.objects.filter(
        asset__agent__bind_project_id=project_id
    ).all()
    IastAssetVulnerabilityDocument().update(list(qs))


def data_correction_all():
    qs = IastVulnerabilityModel.objects.all()
    IastVulnerabilityDocument().update(list(qs))
    qs = Asset.objects.all()
    IastAssetDocument().update(list(qs))
    qs = IastVulAssetRelation.objects.all()
    IastAssetVulnerabilityDocument().update(list(qs))
