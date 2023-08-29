from django.db import migrations


def update_vul_status(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    IastVulnerabilityStatus = apps.get_model("dongtai_common", "IastVulnerabilityStatus")
    IastVulnerabilityStatus(id=7, name="已忽略", name_zh="已忽略", name_en="Ignored").save()


class Migration(migrations.Migration):
    dependencies = [
        ("dongtai_common", "0014_auto_20230828_1132"),
    ]

    operations = [
        migrations.RunPython(update_vul_status),
    ]
