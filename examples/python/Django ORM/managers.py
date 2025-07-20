from django.db import models
from django.db.models import Q

from common import PostSection__SectionStatusChoice
from querysets import PostQuerySet

POST_EDIT_TIMING = "검토중"


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def for_blog(self, blog_id):
        return self.get_queryset().filter(blog_id=blog_id)

    def get_valid_post(self, blog_id: int, data: dict):
        queryset = self.for_blog(blog_id=blog_id).order_by("-posted_at")

        author_ids = data.get("author_ids", "").split(",")
        queryset = queryset.filter(author_id__in=author_ids)


        section_code = data.get("section_code")
        offset = data.get("offset")
        if section_code:
            # offset이 없다면 해당 section을 포함하는 Post만 가져오기
            if not offset:
                queryset = queryset.filter(post_section_set__section_code=section_code)
            # offset이 있다면 해당 section을 포함하는 Post 제외 후 가져오기
            else:
                queryset = queryset.exclude(post_section_set__section_code=section_code)
                data["offset"] -= 1

        # complex filter
        # PostSection 관련 추가 필터 적용
        available_section_status = list()
        match POST_EDIT_TIMING:
            case "검토중":
                available_section_status = [
                    PostSection__SectionStatusChoice.검토중,
                    PostSection__SectionStatusChoice.검토완료,
                    PostSection__SectionStatusChoice.게시됨,
                ]
            case "검토완료":
                available_section_status = [
                    PostSection__SectionStatusChoice.검토완료,
                    PostSection__SectionStatusChoice.게시됨,
                ]

        queryset = queryset.post_section_writable_filter(available_section_status)

        return queryset
