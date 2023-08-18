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
        raise ValidationError(detail=f"污点范围命令必须符合该格式: {PATTERN} .")


def tag_validator(tag: str):
    if not valitate_tag(tag):
        raise ValidationError(detail=f"污点tag必须在以下列表中: {DEFAULT_IAST_VALUE_TAG} .")


def get_validatation_detail_message(e: ValidationError):
    error_text_list = []
    for v in e.detail.values():
        if isinstance(v, (list, tuple)):
            error_text_list.extend(str(error) for error in v)
        elif isinstance(v, dict):
            for error in v.values():
                if isinstance(error, list):
                    error_text_list.extend(str(i) for i in error)
    return "\n".join(error_text_list)
