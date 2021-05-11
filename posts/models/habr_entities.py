from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from posts.models.database import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        default="",
        server_default="",
    )
    password = Column(
        String(128),
        nullable=False,
        default=generate_password_hash("generic_password"),
        server_default=generate_password_hash("generic_password"),
    )
    is_admin = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="0",
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    posts = relationship("Post", back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__} <{self.username}>"

    def __repr__(self):
        return str(self)


class Post(db.Model):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(
        String(300),
        nullable=False,
        default="",
        server_default="",
    )
    published_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now()
    )
    description = Column(Text, nullable=True, default="", server_default="")
    text = Column(Text, nullable=True, default="", server_default="")
    cover_image = Column(String(), nullable=True, default="", server_default="")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship(User, back_populates="posts")
    tags = relationship(
        "Tag", secondary="post_tag_links", back_populates="posts",
    )

    def __str__(self):
        return f"{self.__class__.__name__} <{self.title}>"

    def __repr__(self):
        return str(self)


class Tag(db.Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, default="", server_default="")
    posts = relationship(
        "Post", secondary="post_tag_links", back_populates="tags",
    )

    @hybrid_property
    def posts_number(self):
        return self.posts.count()

    def __str__(self):
        return f"{self.__class__.__name__} <{self.title}>"

    def __repr__(self):
        return str(self)


class PostTagLink(db.Model):
    __tablename__ = "post_tag_links"

    id = Column(Integer, primary_key=True)
    post_id = Column('post_id', Integer, ForeignKey('posts.id'))
    tag_id = Column('tag_id', Integer, ForeignKey('tags.id'))
