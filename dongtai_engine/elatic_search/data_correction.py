from dongtai_common.models.vulnerablity import IastVulnerabilityModel, IastVulnerabilityDocument
from celery import shared_task
from django.apps import apps
from django.db import transaction
from dongtai_common.models.asset import Asset, IastAssetDocument
from dongtai_common.models.asset_vul import IastVulAssetRelation, IastAssetVulnerabilityDocument

from celery.apps.worker import logger


@shared_task
def data_correction_interpetor(situation: str):
    if situation == "project_missing":
        data_correction(-1)


def data_correction(project_id):
    qs = IastVulnerabilityModel.objects.filter(
        agent__bind_project_id=project_id).all()
    IastVulnerabilityDocument().update(list(qs))
    qs = Asset.objects.filter(agent__bind_project_id=project_id).all()
    IastAssetDocument().update(list(qs))
    qs = IastVulAssetRelation.objects.filter(
        asset__agent__bind_project_id=project_id).all()
    IastAssetVulnerabilityDocument().update(list(qs))
