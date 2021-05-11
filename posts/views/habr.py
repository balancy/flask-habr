from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user
from sqlalchemy import desc

from posts.models.database import db
from posts.models.habr_entities import User, Tag, Post
from posts.utils import fill_db_with_data, get_popular_tags

habr_app = Blueprint("habr_app", __name__, url_prefix="/")


@habr_app.route("/", endpoint="posts")
def posts_list():
    posts = db.session.query(Post).order_by(Post.published_at.desc())

    return render_template(
        "posts_list.html",
        title="Все новости",
        posts=posts,
        tags=get_popular_tags(),
        current_user=current_user,
    )


@habr_app.route("/refresh", endpoint="refresh")
def refresh_posts():
    fill_db_with_data()
    return redirect(url_for("habr_app.posts"))


@habr_app.route("/posts/<int:post_id>/", endpoint="details")
def post_details(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    popular_tags = get_popular_tags()

    if not post:
        return render_template("not_found.html", tags=popular_tags)

    return render_template(
        "post_details.html",
        title=post.title,
        post=post,
        tags=popular_tags,
        current_user=current_user,
    )


@habr_app.route("/tags/<int:tag_id>/", endpoint="tag_posts")
def tag_posts(tag_id):
    tag_and_posts = (db.session.query(Tag, Post).filter_by(id=tag_id).
                     join(Post, Tag.posts).order_by(desc(Post.published_at)))
    popular_tags = get_popular_tags()

    if not tag_and_posts:
        return render_template("not_found.html", tags=popular_tags)

    tag = tag_and_posts.first()[0]
    posts = [record[1] for record in tag_and_posts]

    return render_template(
        "tag_posts.html",
        tag=tag,
        title=f"Посты по тегу { tag.title }",
        posts=posts,
        tags=popular_tags,
        current_user=current_user,
    )


@habr_app.route("/users/<int:user_id>/", endpoint="user_posts")
def tag_posts(user_id):
    user_and_posts = (db.session.query(User, Post).filter_by(id=user_id).
                      join(Post, User.posts).order_by(desc(Post.published_at)))
    popular_tags = get_popular_tags()

    if not user_and_posts:
        return render_template("not_found.html", tags=popular_tags)

    user = user_and_posts.first()[0]
    posts = [record[1] for record in user_and_posts]

    return render_template(
        "user_posts.html",
        title=f"Посты пользователя { user.username }",
        user=user,
        current_user=current_user,
        posts=posts,
        tags=popular_tags,
    )


@habr_app.app_errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html")
