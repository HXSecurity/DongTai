from dongtai_common.utils.init_schema import VIEW_CLASS_TO_SCHEMA

from django.core.management.base import BaseCommand
from itertools import count


class Command(BaseCommand):
    help = "Check API schema is complete"

    def handle(self, *args, **options):
        n = count(0)
        for view, schema in VIEW_CLASS_TO_SCHEMA.items():
            for method, schema in schema.items():
                path, path_regex, schema, filepath = schema
                if schema is None:
                    self.stdout.write(self.style.ERROR(f"No schema: {view}"))
                    continue
                has_error = False

                schema_field_check = {schema_field: schema_field in schema for schema_field in ("tags", "summary")}
                if not all(schema_field_check.values()):
                    has_error = True
                    missing_fields = [schema_field for schema_field, exists in schema_field_check.items()]
                    self.stdout.write(
                        self.style.ERROR(
                            f'[{next(n)}]Miss "{missing_fields}" schema: {method} {view} {filepath} {path} {path_regex}'
                        )
                    )
                if not has_error:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{method} {view}: "
                            f"tags: {schema['tags']}, summary: {schema['summary']}"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Check API schema done"))
