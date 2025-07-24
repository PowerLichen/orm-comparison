from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey("blog.id"))
    author_id = Column(Integer, ForeignKey("author.id"))
    title = Column(String(255))
    content = Column(Text)
    posted_at = Column(DateTime)

    sections = relationship("PostSection", back_populates="post")


class PostSection(Base):
    __tablename__ = "post_section"

    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey("blog.id"))
    author_id = Column(Integer, ForeignKey("author.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    content = Column(Text)
    section_code = Column(String(7), unique=True)
    section_status = Column(Integer)
    permit_comment = Column(Boolean, default=False)

    post = relationship("Post", back_populates="sections")