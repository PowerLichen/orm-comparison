class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_base_query(self):
        return self.db.query(Post)

    def filter_by_blog(self, query, blog_id: int):
        return query.filter(Post.blog_id == blog_id)

    def filter_by_authors(self, query, author_ids: list[int]):
        return query.filter(Post.author_id.in_(author_ids)) if author_ids else query

    def filter_by_section_code(self, query, section_code: str, offset: int):
        if not section_code:
            return query
        subq = self.db.query(PostSection.post_id).filter(PostSection.section_code == section_code)
        return query.filter(~Post.id.in_(subq) if offset else Post.id.in_(subq))

    def filter_by_section_status(self, query, allowed_statuses: list[int]):
        return query.filter(
            exists().where(
                (PostSection.post_id == Post.id)
                & (PostSection.permit_comment == True)
                & (PostSection.section_status.in_(allowed_statuses))
            )
        )
