from typing import type_check_only

from rest_framework.request import Request as DRFRequest

from dongtai_common.models.user import User


@type_check_only
class Request(DRFRequest):
    @property
    def user(self) -> User:
        ...

    @user.setter
    def user(self, value) -> None:
        ...
