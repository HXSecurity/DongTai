# Generated by Django 3.2.20 on 2023-07-31 15:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dongtai_common", "0003_auto_20230728_1444"),
    ]

    operations = [
        migrations.AddField(
            model_name="iastassetvulv2",
            name="vul_detail_zh",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="iastassetvulv2",
            name="vul_name_zh",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
