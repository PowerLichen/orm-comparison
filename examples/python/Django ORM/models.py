from django.db import models

from common import PostSection__SectionStatusChoice
from managers import PostManager


class Post(models.Model):
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_at = models.DateTimeField(help_text="실제 게시일자")

    objects = models.Manager()
    service_objects = PostManager()


class PostSection(models.Model):
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_section_set"
    )
    content = models.TextField()
    section_code = models.CharField(
        max_length=7, unique=True, help_text="게시글 섹션에 대한 랜덤 코드"
    )
    section_status = models.IntegerField(
        default=PostSection__SectionStatusChoice.임시저장,
        choices=PostSection__SectionStatusChoice.choices,
    )
    permit_comment = models.BooleanField(
        default=False, help_text="코멘트 작성 가능 여부"
    )
