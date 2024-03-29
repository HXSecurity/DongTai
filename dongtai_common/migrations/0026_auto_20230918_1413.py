# Generated by Django 3.2.20 on 2023-09-18 14:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dongtai_common", "0025_alter_iastagentrequestchainstopographvec_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="affected_versions",
            field=models.JSONField(help_text="影响版本"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="change_time",
            field=models.IntegerField(help_text="修改时间"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="create_time",
            field=models.IntegerField(help_text="创建时间"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="level",
            field=models.IntegerField(
                blank=True,
                choices=[(4, "严重"), (3, "高危"), (2, "中危"), (1, "低危"), (0, "无风险")],
                db_column="level_id",
                default=1,
                help_text="漏洞等级",
            ),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="published_time",
            field=models.IntegerField(help_text="发布时间"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="references",
            field=models.JSONField(default=list, help_text="引用文章"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="unaffected_versions",
            field=models.JSONField(help_text="不影响版本"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="update_time",
            field=models.IntegerField(help_text="更新时间"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="vul_codes",
            field=models.JSONField(help_text="漏洞编号"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="vul_detail",
            field=models.TextField(help_text="漏洞详情"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="vul_detail_zh",
            field=models.TextField(blank=True, help_text="漏洞详情(中文)"),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="vul_id",
            field=models.CharField(blank=True, help_text="漏洞id", max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="vul_name",
            field=models.CharField(blank=True, help_text="漏洞名", max_length=255),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="vul_name_zh",
            field=models.CharField(blank=True, help_text="漏洞名(中文)", max_length=255),
        ),
        migrations.AlterField(
            model_name="iastassetvulv2",
            name="vul_type",
            field=models.JSONField(help_text="漏洞类型"),
        ),
        migrations.AlterField(
            model_name="iastsensitiveinforule",
            name="pattern",
            field=models.TextField(default=""),
        ),
    ]
