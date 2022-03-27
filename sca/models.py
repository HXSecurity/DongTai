from django.db import models

# Create your models here.

from django.db import models


class Package(models.Model):
    aql = models.CharField(max_length=255, blank=True, null=True)
    hash = models.CharField(max_length=255, blank=True, null=True)
    ecosystem = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    license = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'sca2_package'


class Vul(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    summary = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    aliases = models.JSONField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)
    withdrawn = models.DateTimeField(blank=True, null=True)
    references = models.JSONField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'sca2_vul'


class VulPackage(models.Model):
    vul_id = models.CharField(max_length=50, blank=True, null=True)
    ecosystem = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cwe_ids = models.JSONField(blank=True, null=True)
    ghsa = models.CharField(max_length=255, blank=True, null=True)
    cvss_vector = models.CharField(max_length=255, blank=True, null=True)
    cvss_score = models.FloatField(default=0, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    severity = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'sca2_vul_package'


class VulPackageRange(models.Model):
    vul_package_id = models.IntegerField(max_length=11, blank=True, null=True)
    ecosystem = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    introduced = models.CharField(max_length=50, blank=True, null=True)
    fixed = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'sca2_vul_package_range'


class VulPackageVersion(models.Model):
    vul_package_id = models.IntegerField(max_length=11, blank=True, null=True)
    ecosystem = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'sca2_vul_package_version'
