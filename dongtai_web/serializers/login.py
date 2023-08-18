#!/usr/local/env python
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    https://www.django-rest-framework.org/api-guide/fields/
    """

    username = serializers.CharField(
        required=True,
        max_length=12,
        error_messages={"username": _("Username should not be empty")},
    )
    password = serializers.CharField(
        required=True,
        max_length=6,
        error_messages={"password": _("Password should not be blank")},
    )
