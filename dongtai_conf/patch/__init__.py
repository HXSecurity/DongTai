import importlib
import inspect
import logging
import pkgutil
from dataclasses import dataclass
from pathlib import Path
from types import CodeType
from typing import Any, Callable

from dongtai_conf.settings import BASE_DIR

logger = logging.getLogger("patch")


@dataclass
class PatchConfig:
    type_check: bool


is_init_patch = False
PATCH_HANDLER: dict[CodeType, tuple[Callable, PatchConfig]] = {}


def init_patch() -> None:
    global is_init_patch
    if not is_init_patch:
        PATCH_ROOT_PATH = Path(BASE_DIR) / "dongtai_conf" / "patch"
        for module_info in pkgutil.iter_modules([str(PATCH_ROOT_PATH.resolve())]):
            if not module_info.name.startswith("_"):
                importlib.import_module("dongtai_conf.patch." + module_info.name)
        is_init_patch = True
    print(PATCH_HANDLER)


def patch_point(*args) -> Any | None:
    init_patch()
    current_frame = inspect.currentframe()
    if current_frame is None:
        logger.error("current frame is None, can not patch")
        return
    caller_frame = current_frame.f_back
    if caller_frame is None:
        logger.error("caller frame is None, can not patch")
        return
    caller_code = caller_frame.f_code
    if caller_code in PATCH_HANDLER:
        func, patch_config = PATCH_HANDLER[caller_code]
        func_args, _, _, _, kwonlyargs, _, annotations = inspect.getfullargspec(func)

        func_args += kwonlyargs

        if args and len(args) != len(func_args):
            # 如果显式传入参数，进行参数数量检查
            logger.error(f"args number error, expect {len(func_args)}, get {len(args)}")
            return

        patch_func_args = {}
        count = 0
        for name in func_args:
            if name in caller_frame.f_locals:
                local_value = caller_frame.f_locals[name]
                if args and args[count] is not local_value:
                    # 如果显式传入参数，进行参数检查
                    logger.error(
                        f"args error, expect arg name {name}, get value {args[count]}"
                    )
                    return
                if patch_config.type_check:
                    # 如果启用类型检查，进行类型检查
                    type_ = annotations.get(name, None)
                    if type(type_) is type and not isinstance(local_value, type_):
                        logger.error(
                            "type check error, "
                            f"name {name}, expect {type_}, get{type(local_value)}"
                        )
                patch_func_args[name] = local_value
            else:
                logger.error(f"can not call patch function, miss local var {name}")
                return
            count += 1
        return func(**patch_func_args)


def patch(patch_func: Callable, type_check: bool = False):
    def wrapper(func: Callable):
        PATCH_HANDLER[patch_func.__code__] = (func, PatchConfig(type_check=type_check))
        return func

    return wrapper


def check_patch() -> None:
    for code, func in PATCH_HANDLER.items():
        args, _, _, _, kwonlyargs, _, _ = inspect.getfullargspec(func)
        if not set(args + kwonlyargs).issubset(set(code.co_varnames)):
            logger.error(
                f"error: expect args {args + kwonlyargs}, varnames {code.co_varnames}"
            )