import re
from dongtai_conf.settings import DEFAULT_TAINT_VALUE_RANGE_COMMANDS


def valitate_taint_command(command: str) -> bool:
    pattern = rf" *({'|'.join(DEFAULT_TAINT_VALUE_RANGE_COMMANDS)}) *\(( *(P\d+|\d+) *,*)*\) *"
    res = re.fullmatch(pattern, command.upper(), flags=re.IGNORECASE)
    if res:
        return True
    return False
