import os
import re
import logging

from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.drainage import add_trace_message

logger = logging.getLogger("django")
VIEW_CLASS_TO_SCHEMA: dict[type, dict[str, tuple[str, str, dict | None]]] = {}


def init_schema() -> None:
    generator = SchemaGenerator()
    generator._initialise_endpoints()
    endpoints = generator._get_paths_and_endpoints()
    non_trivial_prefix = len(set([view.__class__ for _, _, _, view in endpoints])) > 1
    if non_trivial_prefix:
        path_prefix = os.path.commonpath([path for path, _, _, _ in endpoints])
        path_prefix = re.escape(path_prefix)  # guard for RE special chars in path
    else:
        path_prefix = "/"
    if not path_prefix.startswith("^"):
        path_prefix = "^" + path_prefix  # make sure regex only matches from the start

    for path, path_regex, method, view in endpoints:
        try:
            with add_trace_message(getattr(view, "__class__", view).__name__):
                operation = view.schema.get_operation(
                    path, path_regex, path_prefix, method, generator.registry
                )
                VIEW_CLASS_TO_SCHEMA.setdefault(view.__class__, {})
                VIEW_CLASS_TO_SCHEMA[view.__class__][method.upper()] = (
                    path,
                    path_regex,
                    operation,
                )
        except Exception:
            logger.error(f"unable to get schema: view {view} of path {path}")
