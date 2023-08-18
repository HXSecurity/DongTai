from django.db import models

from dongtai_common.models import User
from dongtai_common.models.project import IastProject
from dongtai_common.utils.db import get_timestamp
from dongtai_common.utils.settings import get_managed


class IastProjectGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    create_time = models.IntegerField(default=get_timestamp)
    create_user = models.ForeignKey(User, models.DO_NOTHING, db_constraint=False, related_name="create_project_group")
    users = models.ManyToManyField(User, through="IastProjectGroupUser")
    projects = models.ManyToManyField(IastProject, through="IastProjectGroupProject")

    class Meta:
        managed = get_managed()
        db_table = "iast_project_group"
        indexes = [models.Index(fields=["name"])]


class IastProjectGroupProject(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(IastProject, models.DO_NOTHING, db_constraint=False)
    project_group = models.ForeignKey(IastProjectGroup, models.DO_NOTHING, db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = "iast_project_group_project"
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "project_group_id"], name="iast_project_group_project_unique_constraint"
            )
        ]
        indexes = [models.Index(fields=["project_group_id", "project_id"])]


class IastProjectGroupUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_constraint=False)
    project_group = models.ForeignKey(IastProjectGroup, models.DO_NOTHING, db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = "iast_project_group_user"
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "project_group_id"], name="iast_project_group_user_unique_constraint"
            )
        ]
        indexes = [models.Index(fields=["project_group_id", "user_id"])]
