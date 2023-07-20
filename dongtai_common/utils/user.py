from django.db.models import Q, QuerySet

from dongtai_common.models.department import Department
from dongtai_common.models.user import User
from dongtai_common.utils import const


def get_auth_users__by_id(user_id: int) -> QuerySet:
    user = User.objects.filter(pk=user_id).first()
    if not user:
        return User.objects.none()
    if user.is_system_admin():
        users = User.objects.all()
    elif user.is_talent_admin():
        talent = user.get_talent()
        departments = talent.departments.all()
        users = User.objects.filter(department__in=departments)
    else:
        users = User.objects.filter(pk=user_id).all()
    return users
