from rest_framework.request import Request as DRFRequest

from dongtai_common.models.user import User


class Request(DRFRequest):
    """used in type check only."""

    @property
    def user(self) -> User:
        ...

    @user.setter
    def user(self, value) -> None:
        ...
