import string
from datetime import datetime

from django.db import models
from shortuuid.django_fields import ShortUUIDField

from dongtai_common.models.assetv2 import AssetV2Global
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.user import User
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils.settings import get_managed


class IastShareTokenStatusChoices(models.IntegerChoices):
    ENABLE = 1, "ENABLE"
    EXPIRE = 2, "EXPIRE"
    DISABLE = 0, "DISABLE"


class IastShareTokenTypeChoices(models.IntegerChoices):
    SCA = 1
    VUL = 2


class IastShareToken(models.Model):
    token = ShortUUIDField(max_length=22, alphabet=string.ascii_letters + string.digits)
    title = models.CharField(max_length=255, blank=True)
    expire_at = models.DateTimeField(blank=True, null=True, help_text="When this time is null, it means indefinitely")
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
    vul = models.ForeignKey(IastVulnerabilityModel, on_delete=models.DO_NOTHING, blank=True, default=-1)
    sca = models.ForeignKey(AssetV2Global, on_delete=models.DO_NOTHING, to_field="aql", blank=True, default="")
    token_type = models.IntegerField(
        default=IastShareTokenTypeChoices.VUL,
        choices=IastShareTokenTypeChoices.choices,
        help_text="".join([f" {i.label}: {i.value} " for i in IastShareTokenTypeChoices]),
    )
    status = models.IntegerField(
        default=IastShareTokenStatusChoices.ENABLE,
        help_text="".join([f" {i.label}: {i.value} " for i in IastShareTokenStatusChoices]),
        choices=IastShareTokenStatusChoices.choices,
    )
    project = models.ForeignKey(IastProject, on_delete=models.CASCADE, blank=True, default=-1)
    project_version = models.ForeignKey(IastProjectVersion, on_delete=models.CASCADE, blank=True, default=-1)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=-1)
    target_url = models.CharField(max_length=255)

    class Meta:
        managed = get_managed()
        db_table = "iast_share_token"

    def get_real_status(self):
        if self.expire_at < datetime.now():
            return IastShareTokenStatusChoices.EXPIRE
        return self.status
