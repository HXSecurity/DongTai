from itertools import count

from django.core.management.base import BaseCommand, CommandError

from dongtai_common.utils.init_schema import VIEW_CLASS_TO_SCHEMA


class Command(BaseCommand):
    help = "Check API schema is complete"

    def handle(self, *args, **options):
        n = count(0)
        has_error = False
        for view, schema__ in VIEW_CLASS_TO_SCHEMA.items():
            for method, schema_ in schema__.items():
                path, path_regex, schema, filepath = schema_
                if schema is None:
                    self.stdout.write(self.style.ERROR(f"No schema: {view}"))
                    continue
                has_error = False

                schema_field_check = {
                    schema_field: schema_field in schema
                    for schema_field in ("tags", "summary")
                }
                if not all(schema_field_check.values()):
                    has_error = True
                    missing_fields = [
                        schema_field
                        for schema_field, exists in schema_field_check.items()
                    ]
                    has_error = True
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

        if has_error:
            raise CommandError
