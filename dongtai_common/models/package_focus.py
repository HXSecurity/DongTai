from django.db import models


class IastPackageFocus(models.Model):
    id = models.BigAutoField(primary_key=True)
    language_id = models.IntegerField()
    package_name = models.CharField(max_length=255)
    package_version = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        db_table = "iast_package_focus"
