
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


def intable_str(value: str):
    try:
        list(map(int, value.split(",")))
    except ValueError as e:
        raise serializers.ValidationError("Not int able after str split") from e


class AggregationArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(
        default=20, min_value=1, help_text=_("Number per page")
    )
    page = serializers.IntegerField(default=1, min_value=1, help_text=_("Page index"))

    order_type = serializers.IntegerField(default=0, help_text=_("Order by"))
    order_type_desc = serializers.IntegerField(default=0, help_text=_("Order by desc"))

    bind_project_id = serializers.IntegerField(
        default=0, help_text=_("bind_project_id")
    )
    project_version_id = serializers.IntegerField(
        default=0, help_text=_("project_version_id")
    )
    uri = serializers.CharField(
        required=False,
        max_length=1024,
    )

    level_id_str = serializers.CharField(
        required=False,
        max_length=12,
        error_messages={"level_str": _("Length limit exceeded")},
        validators=[intable_str],
    )
    project_id_str = serializers.CharField(
        required=False,
        max_length=255,
        error_messages={"project_id_str": _("Length limit exceeded")},
        validators=[intable_str],
    )

    keywords = serializers.CharField(
        required=False,
        max_length=100,
        error_messages={"keywords": _("Length limit exceeded")},
        help_text=_("Keywords select"),
    )

    source_type_str = serializers.CharField(
        required=False,
        max_length=6,
        error_messages={"source_type_str": _("Length limit exceeded")},
        validators=[intable_str],
    )
    availability_str = serializers.CharField(
        required=False,
        max_length=12,
        error_messages={"availability_str": _("Length limit exceeded")},
        validators=[intable_str],
    )
    hook_type_id_str = serializers.CharField(
        required=False,
        max_length=100,
        error_messages={"hook_type_str": _("Length limit exceeded")},
        validators=[intable_str],
    )
    language_str = serializers.CharField(
        required=False,
        max_length=12,
        error_messages={"language_str": _("Length limit exceeded")},
        validators=[intable_str],
    )
    status_id_str = serializers.CharField(
        required=False,
        max_length=12,
        error_messages={"status_id_str": _("Length limit exceeded")},
        validators=[intable_str],
    )
