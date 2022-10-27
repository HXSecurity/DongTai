from django.db import models

# Create your models here.

from django.db import models


from _typeshed import Incomplete
class Package(models.Model):
    huo_xian_product_id: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    aql: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    hash: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    ecosystem: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    version: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    license: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    language: Incomplete = models.CharField(max_length=50, null=False, default='')
    version_publish_time: Incomplete = models.DateTimeField(blank=True, null=True)

    created_at: Incomplete = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at: Incomplete = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table: str = 'sca2_package_v2'


class Vul(models.Model):
    id: Incomplete = models.CharField(primary_key=True, max_length=50)
    summary: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    details: Incomplete = models.TextField(blank=True, null=True)
    aliases: Incomplete = models.JSONField(blank=True, null=True)
    modified: Incomplete = models.DateTimeField(blank=True, null=True)
    published: Incomplete = models.DateTimeField(blank=True, null=True)
    withdrawn: Incomplete = models.DateTimeField(blank=True, null=True)
    references: Incomplete = models.JSONField(null=True)

    created_at: Incomplete = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at: Incomplete = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table: str = 'sca2_vul'


class VulPackage(models.Model):
    cve: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    ecosystem: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    severity: Incomplete = models.CharField(max_length=32, blank=True, null=True)
    introduced: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    introduced_vcode: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    final_version: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    final_vcode: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    fixed: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    fixed_vcode: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    safe_version: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    safe_vcode: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    created_at: Incomplete = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at: Incomplete = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table: str = 'sca2_vul_package_v2'


class VulPackageRange(models.Model):
    vul_package_id: Incomplete = models.IntegerField(blank=True, null=True)
    ecosystem: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    type: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    introduced: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    introduced_vcode: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    fixed: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    fixed_vcode: Incomplete = models.CharField(max_length=50, blank=True, null=True)

    created_at: Incomplete = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at: Incomplete = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table: str = 'sca2_vul_package_range'


class VulPackageVersion(models.Model):
    vul_package_id: Incomplete = models.IntegerField(blank=True, null=True)
    ecosystem: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    version: Incomplete = models.CharField(max_length=255, blank=True, null=True)

    created_at: Incomplete = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at: Incomplete = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table: str = 'sca2_vul_package_version'


class VulCveRelation(models.Model):
    cve: Incomplete = models.CharField(max_length=255)
    cwe: Incomplete = models.CharField(max_length=255)
    cnnvd: Incomplete = models.CharField(max_length=255)
    cnvd: Incomplete = models.CharField(max_length=255)
    ghsa: Incomplete = models.CharField(max_length=255)
    vul_title: Incomplete = models.CharField(max_length=512)
    vul_title_en: Incomplete = models.CharField(max_length=512)
    cwe_info: Incomplete = models.JSONField(blank=True, null=True)
    description: Incomplete = models.JSONField(blank=True, null=True)
    poc: Incomplete = models.JSONField(blank=True, null=True)
    fix_plan: Incomplete = models.JSONField(blank=True, null=True)
    references: Incomplete = models.JSONField(blank=True, null=True)
    cpe_list: Incomplete = models.JSONField(blank=True, null=True)
    cvss2_list: Incomplete = models.JSONField(blank=True, null=True)
    cvss3_list: Incomplete = models.JSONField(blank=True, null=True)
    severity: Incomplete = models.CharField(max_length=32, null=False, default='')
    publish_time: Incomplete = models.DateTimeField(blank=True, null=True)
    update_time: Incomplete = models.DateTimeField(blank=True, null=True)
    created_at: Incomplete = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at: Incomplete = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table: str = 'sca2_cve_relation'


class PackageRepoDependency(models.Model):
    repo_aql: Incomplete = models.CharField(max_length=255, null=False, default='')
    dependency_aql: Incomplete = models.CharField(max_length=255, null=False, default='')

    class Meta:
        db_table: str = 'sca2_package_repo_dependency'


class PackageDependency(models.Model):
    package_name: Incomplete = models.CharField(max_length=255, null=False, default='')
    p_version: Incomplete = models.CharField(max_length=64, null=False, default='')
    dependency_package_name: Incomplete = models.CharField(max_length=255, null=False, default='')
    d_version: Incomplete = models.CharField(max_length=64, null=False, default='')
    ecosystem: Incomplete = models.CharField(max_length=64, null=False, default='')

    class Meta:
        db_table: str = 'sca2_package_dependency'


class PackageLicenseInfo(models.Model):
    license_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    identifier: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    license_text: Incomplete = models.TextField(blank=True, null=True)
    create_at: Incomplete = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_at: Incomplete = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table: str = 'sca2_package_license_info'


class PackageLicenseLevel(models.Model):
    identifier: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    level_id: Incomplete = models.SmallIntegerField(null=False, default=0)
    level_desc: Incomplete = models.CharField(max_length=64, blank=True, null=True)
    create_at: Incomplete = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_at: Incomplete = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table: str = 'sca2_license_level'
