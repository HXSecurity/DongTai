######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : role
# @created     : 星期二 11月 02, 2021 18:01:47 CST
#
# @description :
######################################################################

from django.db import models
from modeltranslation.translator import TranslationOptions, register

from dongtai_common.models.user import User


class IastRole(models.Model):
    name = models.CharField(max_length=255, default="")
    state = models.IntegerField(
        default=0,
    )

    class Meta:
        db_table = "web_role"


class WebAPIRoute(models.Model):
    name = models.CharField(max_length=255, default="")
    path = models.CharField(max_length=255, default="")
    method = models.CharField(max_length=255, default="")

    class Meta:
        db_table = "webapi_api_site"


class IastRoleAPIRelation(models.Model):
    api = models.ForeignKey(to=WebAPIRoute, on_delete=models.CASCADE, db_constraint=False)
    role = models.ForeignKey(to=IastRole, on_delete=models.CASCADE, db_constraint=False)

    state = models.IntegerField(default=2)

    class Meta:
        db_table = "web_api_role_relation"


class IastRoleUserRelation(models.Model):
    role = models.ForeignKey(to=IastRole, on_delete=models.CASCADE, db_constraint=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = "web_role_user_relation"


#    route = WebAPIRoute.objects.filter(path=resolve_macth.route,
#                                       method=request.method).first()
#    if role_rel:
#            api=route, role=role_rel.role).first()
#    if permission:


class WebURLRoute(models.Model):
    name = models.CharField(max_length=255, default="")
    path = models.CharField(max_length=255, default="")
    component = models.CharField(max_length=255, default="")
    meta_keepAlive = models.CharField(max_length=255, default="")
    meta_disabled = models.CharField(max_length=255, default="")
    meta_i18n = models.CharField(max_length=255, default="")
    meta_isMenu = models.CharField(max_length=255, default="")
    meta_name = models.CharField(max_length=255, default="")
    redirect = models.CharField(max_length=255, default="")
    name_i18n = models.CharField(max_length=255, default="")
    parent = models.IntegerField(default=0)

    class Meta:
        db_table = "web_url_route"


class WebButtonRoute(models.Model):
    name = models.CharField(max_length=255, default="")
    webroute = models.ForeignKey(to=WebURLRoute, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = "web_button"


class IastButtonAPIRelation(models.Model):
    api = models.ForeignKey(to=WebAPIRoute, on_delete=models.CASCADE, db_constraint=False)
    button = models.ForeignKey(to=WebButtonRoute, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = "web_api_button_relation"


class IastRoleButtonRelation(models.Model):
    role = models.ForeignKey(to=IastRole, on_delete=models.CASCADE, db_constraint=False)
    button = models.ForeignKey(to=WebButtonRoute, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = "web_role_button_relation"


class IastRoleURlRelation(models.Model):
    role = models.ForeignKey(to=IastRole, on_delete=models.CASCADE, db_constraint=False)
    url = models.ForeignKey(to=WebURLRoute, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = "web_role_url_relation"


@register(WebURLRoute)
class WebURLRouteOptions(TranslationOptions):
    fields = ("name_i18n",)
