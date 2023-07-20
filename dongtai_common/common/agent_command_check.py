import re

from rest_framework.serializers import ValidationError

from dongtai_conf.settings import (
    DEFAULT_IAST_VALUE_TAG,
    DEFAULT_TAINT_VALUE_RANGE_COMMANDS,
)

PATTERN = rf" *({'|'.join(DEFAULT_TAINT_VALUE_RANGE_COMMANDS)}) *\(( *(P\d+|\d+) *,*)*\) *"


def valitate_taint_command(command: str) -> bool:
    res = re.fullmatch(PATTERN, command.upper(), flags=re.IGNORECASE)
    if res:
        return True
    return False


def valitate_tag(tag: str) -> bool:
    if tag not in DEFAULT_IAST_VALUE_TAG:
        return False
    return True


def taint_command_validator(command: str):
    if not valitate_taint_command(command):
        raise ValidationError(f"The command must fit {PATTERN} .")


def tag_validator(tag: str):
    if not valitate_tag(tag):
        raise ValidationError(f"The tag must in {DEFAULT_IAST_VALUE_TAG} .")
