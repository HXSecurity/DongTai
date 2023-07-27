from django.db import models

from dongtai_common.models import User
from dongtai_common.models.project import IastProject
from dongtai_common.utils.db import get_timestamp
from dongtai_common.utils.settings import get_managed


class IastProjectGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    create_time = models.IntegerField(default=get_timestamp)
    create_user = models.ForeignKey(User, models.DO_NOTHING, db_constraint=False, related_name="create_project_group")
    users = models.ManyToManyField(User, through="IastProjectGroupUser")
    projects = models.ManyToManyField(IastProject, through="IastProjectGroupProject")

    class Meta:
        managed = get_managed()
        db_table = "iast_project_group"


class IastProjectGroupProject(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(IastProject, models.DO_NOTHING, db_constraint=False)
    project_group = models.ForeignKey(IastProjectGroup, models.DO_NOTHING, db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = "iast_project_group_project"


class IastProjectGroupUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_constraint=False)
    project_group = models.ForeignKey(IastProjectGroup, models.DO_NOTHING, db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = "iast_project_group_user"
