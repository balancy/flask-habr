from flask import Blueprint, request, render_template, url_for, redirect
from sqlalchemy import func, desc, asc
from sqlalchemy.orm import lazyload
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from sqlalchemy.exc import IntegrityError

from posts.models.database import db
from posts.models.habr_entities import User, Tag, PostTagLink, Post
from posts.utils import fill_db_with_data

habr_app = Blueprint("habr_app", __name__, url_prefix="/")


@habr_app.route("/", endpoint="posts")
def posts_list():
    posts = db.session.query(Post).order_by(Post.published_at.desc())
    title = "Все новости"
    all_tags = db.session.query(Tag).all()

    # new_tags = (db.session.query(Tag, func.count(posts.c.post_id).label("posts_count")).
    #             join(posts).group_by(Post).order_by("posts_count DESC"))
    # new_tags = db.session.query(Tag, Tag.posts_number).order_by(Tag.posts_number.desc())

    return render_template(
        "posts_list.html",
        title=title,
        posts=posts,
        tags=all_tags,
    )


@habr_app.route("/refresh", endpoint="refresh")
def refresh_posts():
    fill_db_with_data()
    return redirect(url_for("habr_app.posts"))


@habr_app.route("/posts/<int:post_id>/", endpoint="details")
def post_details(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    all_tags = db.session.query(Tag).all()

    if not post:
        return render_template("not_found.html", tags=all_tags)

    return render_template(
        "post_details.html",
        title=post.title,
        post=post,
        tags=all_tags,
    )


@habr_app.route("/tags/<int:tag_id>/", endpoint="tag_posts")
def tag_posts(tag_id):
    tags_and_posts = (db.session.query(Tag, Post).filter_by(id=tag_id).
                      join(Post, Tag.posts).order_by(desc(Post.published_at)))
    all_tags = db.session.query(Tag).all()

    if not tags_and_posts:
        return render_template("not_found.html", tags=all_tags)

    tag = tags_and_posts.first()[0]
    posts = [record[1] for record in tags_and_posts]

    return render_template(
        "tag_posts.html",
        tag=tag,
        title=f"Посты по тегу { tag.title }",
        posts=posts,
        tags=all_tags,
    )


@habr_app.route("/users/<int:user_id>/", endpoint="user_posts")
def tag_posts(user_id):
    user_and_posts = (db.session.query(User, Post).filter_by(id=user_id).
                      join(Post, User.posts).order_by(desc(Post.published_at)))
    all_tags = db.session.query(Tag).all()

    if not user_and_posts:
        return render_template("not_found.html", tags=all_tags)

    user = user_and_posts.first()[0]
    posts = [record[1] for record in user_and_posts]

    return render_template(
        "user_posts.html",
        title=f"Посты пользователя { user.username }",
        user=user,
        posts=posts,
        tags=all_tags,
    )


@habr_app.app_errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html")

# @habr_app.route("/add/", methods=["GET", "POST"], endpoint="add")
# def add_product():
#     if request.method == "GET":
#         return render_template("products/add_product.html")
#     product_name = request.form.get("product-name")
#     if not product_name:
#         raise BadRequest("Product name is required")
#
#     if Product.query.filter_by(name=product_name).count():
#         raise BadRequest(
#             f"Error adding product {product_name!r}. Product already exists!")
#
#     product_is_new = request.form.get("is-new")
#     product = Product(name=product_name, is_new=bool(product_is_new))
#     db.session.add(product)
#     try:
#         db.session.commit()
#     except IntegrityError:
#         db.session.rollback()
#         raise InternalServerError(
#             f"Error adding product {product_name!r}.")
#
#     product_url = url_for("products_app.details", product_id=product.id)
#     return redirect(product_url)
#
#
# @habr_app.route("/<int:product_id>/", endpoint="details")
# def product_details(product_id):
#     # product = Product.query.filter(Product.id == product_id).one_or_none()
#     product = Product.query.filter_by(id=product_id).one_or_none()
#     if product is None:
#         raise NotFound(f"Product #{product_id} not found!")
#
#     return render_template(
#         "products/product_details.html",
#         product=product,
#     )
