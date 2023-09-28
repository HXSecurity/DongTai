import tantivy
from celery import shared_task

from dongtai_common.models.vulnerablity import IastVulnerabilityModel, tantivy_index


@shared_task(queue="dongtai-periodic-task")
def update_vul_tantivy_index():
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
    ]
    vul_data = list(queryset.values(*tuple(fields)))
    for vul in vul_data:
        title = f"{vul['uri']} {vul['http_method']} 出现 {vul['strategy__vul_name']}"
        if vul["taint_position"]:
            title += " 位置:" + vul["taint_position"]

        writer.add_document(
            tantivy.Document(
                id=vul["id"],
                title=title,
                project_id=vul["project_id"],
                project_version_id=vul["project_version_id"],
                uri=vul["uri"],
                strategy_id=vul["strategy_id"],
                level_id=vul["level_id"],
                status_id=vul["status_id"],
            )
        )

    writer.commit()
