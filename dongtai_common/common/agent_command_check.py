import re
from dongtai_conf.settings import DEFAULT_TAINT_VALUE_RANGE_COMMANDS, DEFAULT_IAST_VALUE_TAG

def valitate_taint_command(command: str) -> bool:
    pattern = rf" *({'|'.join(DEFAULT_TAINT_VALUE_RANGE_COMMANDS)}) *\(( *(P\d+|\d+) *,*)*\) *"
    res = re.fullmatch(pattern, command.upper(), flags=re.IGNORECASE)
    if res:
        return True
    return False


def valitate_tag(tag: str) -> bool:
    if tag not in DEFAULT_IAST_VALUE_TAG:
        return False
    return True
