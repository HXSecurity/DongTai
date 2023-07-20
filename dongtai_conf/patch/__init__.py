import importlib
import inspect
import logging
import pkgutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from types import CodeType
from typing import Any, Callable, TypeVar, overload

from typing_extensions import TypeVarTuple, Unpack

from dongtai_conf.settings import BASE_DIR

logger = logging.getLogger("patch")


@dataclass
class PatchConfig:
    type_check: bool


is_init_patch = False
PATCH_HANDLER: dict[CodeType, dict[int, tuple[Callable, PatchConfig]]] = defaultdict(
    dict
)


def init_patch() -> None:
    global is_init_patch
    if not is_init_patch:
        PATCH_ROOT_PATH = Path(BASE_DIR) / "dongtai_conf" / "patch"
        for module_info in pkgutil.iter_modules([str(PATCH_ROOT_PATH.resolve())]):
            if not module_info.name.startswith("_"):
                importlib.import_module("dongtai_conf.patch." + module_info.name)
        is_init_patch = True
    print(PATCH_HANDLER)


T = TypeVar("T")
Ts = TypeVarTuple("Ts")


@overload
def patch_point(*args: Unpack[tuple[T]], patch_id: int = 0) -> T:
    ...


@overload
def patch_point(*args: Unpack[Ts], patch_id: int = 0) -> tuple[Unpack[Ts]]:
    ...


def patch_point(*args: Any, patch_id: int = 0) -> Any:
    init_patch()
    current_frame = inspect.currentframe()
    if current_frame is None:
        logger.error("current frame is None, can not patch")
        return _return_args(*args)
    caller_frame = current_frame.f_back
    if caller_frame is None:
        logger.error("caller frame is None, can not patch")
        return _return_args(*args)
    caller_code = caller_frame.f_code
    if caller_code in PATCH_HANDLER:
        func, patch_config = PATCH_HANDLER[caller_code][patch_id]
        func_args, _, _, _, kwonlyargs, _, annotations = inspect.getfullargspec(func)
        func_args += kwonlyargs

        patch_func_args = {}
        for name in func_args:
            if name in caller_frame.f_locals:
                local_value = caller_frame.f_locals[name]
                if patch_config.type_check:
                    # 如果启用类型检查,进行类型检查
                    type_ = annotations.get(name, None)
                    if type(type_) is type and not isinstance(local_value, type_):
                        logger.error(
                            "type check error, "
                            f"name {name}, expect {type_}, get{type(local_value)}"
                        )
                patch_func_args[name] = local_value
            else:
                logger.error(f"can not call patch function, miss local var {name}")
                return _return_args(*args)
        return_value = func(**patch_func_args)
        if return_value is None:
            return _return_args(*args)
        elif len(args) == 1:
            return return_value
        elif not isinstance(return_value, tuple):
            logger.error(
                f"return value type error: expect tuple, get {type(return_value)}"
            )
            return _return_args(*args)
        elif len(return_value) != len(args):
            logger.error(
                f"return value len error: expect {len(args)}, get {len(return_value)}"
            )
            return _return_args(*args)
        else:
            return _return_args(*return_value)
    return _return_args(*args)


def _return_args(*args: Unpack[Ts]) -> tuple[Unpack[Ts]] | Any:
    print(args)
    if len(args) == 1:
        return args[0]
    return args


def patch(patch_func: Callable, type_check: bool = False, patch_id: int = 0):
    def wrapper(func: Callable):
        PATCH_HANDLER[patch_func.__code__][patch_id] = (
            func,
            PatchConfig(type_check=type_check),
        )
        return func

    return wrapper


def check_patch() -> None:
    for code, func in PATCH_HANDLER.items():
        args, _, _, _, kwonlyargs, _, _ = inspect.getfullargspec(func)
        if not set(args + kwonlyargs).issubset(set(code.co_varnames)):
            logger.error(
                f"error: expect args {args + kwonlyargs}, varnames {code.co_varnames}"
            )
