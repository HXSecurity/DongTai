# Generated by Django 3.2.20 on 2023-10-07 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dongtai_common", "0032_update_vul_index_task"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="ldap_dn",
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.ForeignKey(
                db_constraint=False,
                default=2,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="dongtai_common.iastrolev2",
            ),
        ),
    ]