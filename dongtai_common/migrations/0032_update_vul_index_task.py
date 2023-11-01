from django.db import migrations


def update_vul_index_task(apps, schema_editor):
    from django_celery_beat.models import IntervalSchedule, PeriodicTask

    obj = IntervalSchedule.objects.create(id=8, every=30, period=IntervalSchedule.MINUTES)
    PeriodicTask.objects.create(
        name="update_vul_tantivy_index",
        task="dongtai_web.aggr_vul.tasks.update_vul_tantivy_index",
        enabled=True,
        interval=obj,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("dongtai_common", "0031_auto_20230926_1510"),
    ]

    operations = [
        migrations.RunPython(update_vul_index_task),
    ]
