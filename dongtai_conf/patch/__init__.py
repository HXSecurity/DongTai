import importlib
import logging
import pkgutil
from collections import defaultdict
from collections.abc import Callable
from contextvars import ContextVar
from functools import wraps
from pathlib import Path
from typing import Any, TypeVar, overload

from typing_extensions import TypeVarTuple, Unpack

from dongtai_conf.settings import BASE_DIR

logger = logging.getLogger("dongtai.openapi")


is_init_patch = False
PATCH_HANDLER: dict[Callable[..., Any], dict[int, Callable[..., Any]]] = defaultdict(dict)

context_func: ContextVar[Callable[..., Any] | None] = ContextVar("context_func", default=None)
context_count: ContextVar[int] = ContextVar("context_count", default=0)


def init_patch() -> None:
    global is_init_patch  # noqa: PLW0603
    if not is_init_patch:
        PATCH_ROOT_PATH = Path(BASE_DIR) / "dongtai_conf" / "patch"
        for module_info in pkgutil.iter_modules([str(PATCH_ROOT_PATH.resolve())]):
            if not module_info.name.startswith("_"):
                importlib.import_module("dongtai_conf.patch." + module_info.name)
                logger.info(f"load patch dongtai_conf.patch.{module_info.name}")
        is_init_patch = True


T = TypeVar("T")
Ts = TypeVarTuple("Ts")


@overload
def patch_point(*args: Unpack[tuple[T]]) -> T:
    ...


@overload
def patch_point(*args: Unpack[Ts]) -> tuple[Unpack[Ts]]:
    ...


def patch_point(*args: Any) -> Any:
    init_patch()
    patch_func = context_func.get()
    patch_id = context_count.get()
    context_count.set(patch_id + 1)
    logger.debug(f"run patch on function: {patch_func} id: {patch_id}")
    if patch_func in PATCH_HANDLER:
        func = PATCH_HANDLER[patch_func][patch_id]
        return_value = func(*args)
        if return_value is None:
            return _return_args(*args)
        if len(args) == 1:
            return return_value
        if not isinstance(return_value, tuple):
            logger.error(f"return value type error: expect tuple, get {type(return_value)}")
            return _return_args(*args)
        if len(return_value) != len(args):
            logger.error(f"return value len error: expect {len(args)}, get {len(return_value)}")
            return _return_args(*args)
        return _return_args(*return_value)
    return _return_args(*args)


def _return_args(*args: Unpack[Ts]) -> tuple[Unpack[Ts]] | Any:
    if len(args) == 1:
        return args[0]
    return args


def to_patch(to_patch_func: Callable[..., Any]):
    @wraps(to_patch_func)
    def wrapper(*args: Any, **kwargs: Any):
        token_func = context_func.set(to_patch_func)
        token_count = context_count.set(0)
        try:
            return to_patch_func(*args, **kwargs)
        finally:
            context_func.reset(token_func)
            context_count.reset(token_count)

    wrapper.to_patch_func = to_patch_func  # type: ignore
    return wrapper


def patch(patch_func: Callable[..., Any], patch_id: int = 0):
    @overload
    def wrapper(func: Callable[[Unpack[tuple[T]]], T]):
        ...

    @overload
    def wrapper(func: Callable[[Unpack[Ts]], tuple[Unpack[Ts]]]):
        ...

    def wrapper(func: Callable[..., Any]):
        to_patch_func = getattr(patch_func, "to_patch_func", None)
        if to_patch_func is None:
            logger.error(f"to patch function {patch_func} must be decorated by @to_patch")
        else:
            PATCH_HANDLER[to_patch_func][patch_id] = func
        return func

    return wrapper
