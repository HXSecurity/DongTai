# Generated by Django 3.2.20 on 2023-08-03 14:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dongtai_common", "0005_iastprojectmetadata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="iastprojectgroup",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="iastrolev2",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AddIndex(
            model_name="iastprojectgroup",
            index=models.Index(fields=["name"], name="iast_projec_name_336825_idx"),
        ),
        migrations.AddIndex(
            model_name="iastrolev2",
            index=models.Index(fields=["name"], name="iast_role_name_711a1a_idx"),
        ),
    ]