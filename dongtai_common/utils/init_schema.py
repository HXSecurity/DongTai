import inspect
import logging
import os
import re

from drf_spectacular.drainage import add_trace_message
from drf_spectacular.generators import SchemaGenerator

logger = logging.getLogger("django")
VIEW_CLASS_TO_SCHEMA: dict[type, dict[str, tuple[str, str, dict | None, str]]] = {}


def init_schema() -> None:
    generator = SchemaGenerator()
    generator._initialise_endpoints()
    endpoints = generator._get_paths_and_endpoints()
    non_trivial_prefix = len({view.__class__ for _, _, _, view in endpoints}) > 1
    if non_trivial_prefix:
        path_prefix = os.path.commonpath([path for path, _, _, _ in endpoints])
        path_prefix = re.escape(path_prefix)  # guard for RE special chars in path
    else:
        path_prefix = "/"
    if not path_prefix.startswith("^"):
        path_prefix = "^" + path_prefix  # make sure regex only matches from the start
    from dongtai_common.endpoint import EndPoint

    for path, path_regex, method, view in endpoints:
        if not issubclass(view.__class__, EndPoint):
            continue
        try:
            filepath = inspect.getfile(view.__class__)
            with add_trace_message(getattr(view, "__class__", view).__name__):
                operation = view.schema.get_operation(
                    path, path_regex, path_prefix, method, generator.registry
                )
                VIEW_CLASS_TO_SCHEMA.setdefault(view.__class__, {})
                VIEW_CLASS_TO_SCHEMA[view.__class__][method.upper()] = (
                    path,
                    path_regex,
                    operation,
                    filepath,
                )
        except Exception as e:
            logger.debug(
                f"unable to get schema: view {view} of path {path}", exc_info=e
            )
