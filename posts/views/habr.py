from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required
from sqlalchemy import desc

from posts.models.database import db
from posts.models.habr_entities import User, Tag, Post
from posts.utils import fill_db_with_data, get_popular_tags

habr_app = Blueprint("habr_app", __name__, url_prefix="/")


@habr_app.route("/", endpoint="posts")
def posts_list():
    """View for all posts.

    :return: rendered template
    """

    posts = db.session.query(Post).order_by(Post.published_at.desc())

    return render_template(
        "posts_list.html",
        title="Все новости",
        posts=posts,
        tags=get_popular_tags(),
        current_user=current_user,
    )


@habr_app.route("/refresh", endpoint="refresh")
@login_required
def refresh_posts():
    """Refreshes list of posts on main page.

    :return: redirect to main page
    """

    fill_db_with_data()
    return redirect(url_for("habr_app.posts"))


@habr_app.route("/posts/<int:post_id>/", endpoint="details")
def post_details(post_id):
    """View for one post in details.

    :param post_id: id of post
    :return: rendered template
    """

    popular_tags = get_popular_tags()
    post = db.session.query(Post).filter_by(id=post_id).first()

    if post is None:
        return render_template(
            "not_found.html",
            title=f"Пост c id = {post_id} не найден в БД",
            tags=popular_tags,
        )

    return render_template(
        "post_details.html",
        title=post.title,
        post=post,
        tags=popular_tags,
        current_user=current_user,
    )


@habr_app.route("/tags/<int:tag_id>/", endpoint="tag_posts")
def tag_posts(tag_id):
    """View for posts that have specified tag.

    :param tag_id: id of tag
    :return: rendered template
    """

    popular_tags = get_popular_tags()
    tag_and_posts = (db.session.query(Tag, Post).filter_by(id=tag_id).
                     join(Post, Tag.posts).order_by(desc(Post.published_at)))

    if (result_first_row := tag_and_posts.first()) is None:
        return render_template(
            "not_found.html",
            title=f"Тег c id = {tag_id} не найден в БД",
            tags=popular_tags,
        )

    return render_template(
        "tag_posts.html",
        tag=result_first_row[0],
        title=f"Посты по тегу { result_first_row[0].title }",
        posts=[record[1] for record in tag_and_posts],
        tags=popular_tags,
        current_user=current_user,
    )


@habr_app.route("/users/<int:user_id>/", endpoint="user_posts")
def user_posts(user_id):
    """View for posts published by specified user.

    :param user_id: id of user
    :return: rendered template
    """

    popular_tags = get_popular_tags()

    user_and_posts = (db.session.query(User, Post).filter_by(id=user_id).
                      join(Post, User.posts).order_by(desc(Post.published_at)))

    if (result_first_row := user_and_posts.first()) is None:
        return render_template(
            "not_found.html",
            title=f"Пользователь c id = {user_id} не найден в БД",
            tags=popular_tags,
        )

    return render_template(
        "user_posts.html",
        title=f"Посты пользователя { result_first_row[0].username }",
        user=result_first_row[0],
        current_user=current_user,
        posts=[result[1] for result in user_and_posts],
        tags=popular_tags,
    )


@habr_app.app_errorhandler(404)
def page_not_found(e):
    """Handling not found page.

    :return: rendered template
    """

    return render_template(
        "not_found.html",
        title="Страница не найдена",
    )
