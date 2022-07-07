from abc import ABC

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import ValidationError


class AggregationArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         min_value=1,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1,
                                    min_value=1,
                                    help_text=_('Page index'))

    order_type = serializers.IntegerField(default=0, help_text=_('Order by'))
    order_type_desc = serializers.IntegerField(default=0, help_text=_('Order by desc'))

    bind_project_id = serializers.IntegerField(default=0, help_text=_('bind_project_id'))
    project_version_id = serializers.IntegerField(default=0, help_text=_('project_version_id'))

    level_id_str = serializers.CharField(
        required=False,
        max_length=12,
        error_messages={
            "level_str": _("Length limit exceeded")
        }
    )
    project_id_str = serializers.CharField(
        required=False,
        max_length=255,
        error_messages={
            "project_id_str": _("Length limit exceeded")
        }
    )

    keywords = serializers.CharField(
        required=False,
        max_length=100,
        error_messages={
            "keywords": _("Length limit exceeded")
        },
        help_text=_('Keywords select')
    )

    source_type_str = serializers.CharField(
        required=False,
        max_length=6,
        error_messages={
            "source_type_str": _("Length limit exceeded")
        }
    )
    availability_str = serializers.CharField(
        required=False,
        max_length=12,
        error_messages={
            "availability_str": _("Length limit exceeded")
        }
    )
    hook_type_id_str = serializers.CharField(
        required=False,
        max_length=100,
        error_messages={
            "hook_type_str": _("Length limit exceeded")
        }
    )
    language_str = serializers.CharField(
        required=False,
        max_length=12,
        error_messages={
            "language_str": _("Length limit exceeded")
        }
    )
    status_id_str = serializers.CharField(
        required=False,
        max_length=12,
        error_messages={
            "status_id_str": _("Length limit exceeded")
        }
    )
