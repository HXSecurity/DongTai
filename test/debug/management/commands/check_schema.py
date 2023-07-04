from dongtai_common.utils.init_schema import VIEW_CLASS_TO_SCHEMA

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Check API schema is complete"

    def handle(self, *args, **options):
        count = 0
        for view, schema in VIEW_CLASS_TO_SCHEMA.items():
            for method, schema in schema.items():
                _, _, schema = schema
                if schema is None:
                    self.stdout.write(self.style.ERROR(f"No schema: {view}"))
                    continue
                has_error = False
                for schema_field in ("tags", "summary"):
                    if not schema.get(schema_field, None):
                        has_error = True
                        count += 1
                        self.stdout.write(
                            self.style.ERROR(
                                f'[{count}]Miss "{schema_field}" schema: {method} {view}'
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
