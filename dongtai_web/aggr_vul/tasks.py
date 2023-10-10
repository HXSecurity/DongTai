import logging

import tantivy
from celery import shared_task
from celery_singleton import Singleton
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from dongtai_common.models.vulnerablity import IastVulnerabilityModel, tantivy_index
from dongtai_conf.settings import TANTIVY_STATE

logger = logging.getLogger("dongtai-core")


@receiver(post_delete, sender=IastVulnerabilityModel, dispatch_uid="update_vul_tantivy_index")
@receiver(post_save, sender=IastVulnerabilityModel, dispatch_uid="update_vul_tantivy_index")
@receiver(m2m_changed, sender=IastVulnerabilityModel, dispatch_uid="update_vul_tantivy_index")
def update_vul_tantivy_index_receiver(sender, instance, **kwargs):
    update_vul_tantivy_index.apply_async(countdown=120)


@shared_task(
    queue="dongtai-periodic-task",
    base=Singleton,
    lock_expiry=20,
)
def update_vul_tantivy_index():
    if not TANTIVY_STATE:
        return
    try:
        logger.info("Start update vul tantivy index")
        index = tantivy_index()
        writer = index.writer()
        writer.delete_all_documents()

        queryset = IastVulnerabilityModel.objects.filter(is_del=0, project_id__gt=0)
        fields = [
            "id",
            "project_id",
            "project_version_id",
            "uri",
            "strategy_id",
            "level_id",
            "status_id",
            "http_method",
            "strategy__vul_name",
            "taint_position",
            "first_time",
            "latest_time",
        ]
        vul_data = list(queryset.values(*tuple(fields)))
        for vul in vul_data:
            title = f"{vul['uri']} {vul['http_method']} 出现 {vul['strategy__vul_name']}"
            if vul["taint_position"]:
                title += " 位置:" + vul["taint_position"]

            doc = tantivy.Document()
            doc.add_unsigned("id", vul["id"])
            doc.add_text("title", title)
            doc.add_unsigned("project_id", vul["project_id"])
            doc.add_unsigned("project_version_id", vul["project_version_id"])
            doc.add_text("uri", vul["uri"])
            doc.add_unsigned("strategy_id", vul["strategy_id"])
            doc.add_unsigned("level_id", vul["level_id"])
            doc.add_unsigned("status_id", vul["status_id"])
            doc.add_unsigned("first_time", vul["first_time"])
            doc.add_unsigned("latest_time", vul["latest_time"])

            writer.add_document(doc)

        writer.commit()

        logger.info("Update vul tantivy index success!")
    except Exception:
        logger.exception("Create index error")
