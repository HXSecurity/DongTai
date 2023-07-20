######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : utils
# @created     : Monday Sep 27, 2021 18:03:20 CST
#
# @description :
######################################################################


from random import choice
from rest_framework.serializers import ChoiceField
from faker import Faker
from rest_framework.serializers import SerializerMetaclass
from rest_framework.serializers import CharField, IntegerField
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

fake = Faker()


def _datagen_serializer(ser):
    fields = ser.get_fields()
    data = {}
    for field in fields:
        data[field] = data_gen_route(fields[field])
    return data


def data_gen_route(obj):
    if isinstance(obj, IntegerField):
        return _datagen_int(obj)
    elif isinstance(obj, CharField):
        return _datagen_char(obj)
    elif isinstance(obj, ChoiceField):
        return _datagen_choice(obj)
    elif isinstance(obj, serializers.Serializer):
        return _datagen_serializer(obj)
    print(type(obj))


def _datagen_int(field: IntegerField) -> int:
    max_value = 255
    min_value = -255
    if hasattr(field, "max_value") and field.max_value is not None:
        max_value = field.max_value
    if hasattr(field, "min_value") and field.min_value is not None:
        min_value = field.min_value
    return fake.pyint(min(max_value, min_value), max(max_value, min_value))


def _datagen_char(field: CharField) -> str:
    max_length = 255
    min_length = 0
    if hasattr(field, "max_length") and field.max_length is not None:
        max_length = field.max_length
    if hasattr(field, "min_length") and field.min_length is not None:
        min_length = field.min_length
    return fake.pystr(min(max_length, min_length), max(max_length, min_length))


def _datagen_choice(field: ChoiceField):
    return choice(list(field.choices.values()))
