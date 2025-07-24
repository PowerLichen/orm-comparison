from models import Post
from repositories import PostRepository

class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    def get_valid_posts(self, blog_id: int, data: dict):
        author_ids = (
            [int(a) for a in data.get("author_ids", "").split(",") if a]
            if data.get("author_ids")
            else []
        )
        section_code = data.get("section_code")
        offset = int(data.get("offset", 0))
        edit_timing = 0  # 검토중

        allowed_statuses = [0]
        match edit_timing:
            case "검토중":
                allowed_statuses.extend(
                    [SectionStatus.검토중, SectionStatus.검토완료, SectionStatus.게시됨]
                )
            case "검토완료":
                allowed_statuses.extend([SectionStatus.검토완료, SectionStatus.게시됨])
            case _:
                pass

        q = self.repo.get_base_query()
        q = self.repo.filter_by_blog(q, blog_id)
        q = self.repo.filter_by_authors(q, author_ids)
        q = self.repo.filter_by_section_code(q, section_code, offset)
        q = self.repo.filter_by_section_status(q, allowed_statuses)

        return q.order_by(Post.posted_at.desc()).offset(offset).limit(10).all()
