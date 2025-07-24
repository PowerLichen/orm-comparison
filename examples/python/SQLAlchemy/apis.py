from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from services import PostService
from schemas import PostOut
from database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/valid", response_model=list[PostOut])
def get_valid_posts(
    blog_id: int,
    author_ids: str = Query(default=""),
    section_code: str = Query(default=None),
    offset: int = Query(default=0),
    edit_timing: str = Query(default="검토중"),
    db: Session = Depends(get_db),
):
    data = {
        "author_ids": author_ids,
        "section_code": section_code,
        "offset": offset,
        "edit_timing": edit_timing,
    }
    return PostService.get_valid_posts(db, blog_id, data)