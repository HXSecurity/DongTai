# Generated by Django 3.2.20 on 2023-08-22 12:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dongtai_common", "0012_session"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="failed_login_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="failed_login_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
