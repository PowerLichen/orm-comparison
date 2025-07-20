from dataclasses import dataclass

from django.db import models
from django.db.models import Q


class PostSection__SectionStatusChoice(models.IntegerChoices):
    임시저장 = 10, "임시저장"
    검토중 = 20, "검토중"
    검토완료 = 21, "검토완료"
    게시됨 = 30, "게시됨"
    미검증 = 101, "미검증, 랜덤 작성된 section"
