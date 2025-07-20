from dataclasses import dataclass
from django.db import models
from django.db.models import Count, Q

from common import PostSection__SectionStatusChoice


class PostQuerySet(models.QuerySet):
    def post_section_writable_filter(self, section_status__in: list = None):
        if section_status__in is None:
            section_status__in = list()

        queryset = self.annotate(
            section_count=Count(
                "post_section_set",
                filter=Q(
                    post_section_set__permit_comment=True,
                    post_section_set__section_status__in=[
                        PostSection__SectionStatusChoice.미검증,
                        *section_status__in,
                    ],
                ),
            )
        )

        return queryset.filter(section_count__gt=0)
