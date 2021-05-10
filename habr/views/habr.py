from flask import Blueprint, request, render_template, url_for, redirect
from sqlalchemy import func
from sqlalchemy.orm import lazyload
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from sqlalchemy.exc import IntegrityError

from habr.models.database import db
from habr.models.habr_entities import User, Tag, PostTagLink, Post
from habr.utils import fill_db_with_data

habr_app = Blueprint("habr_app", __name__, url_prefix="/")


@habr_app.route("/", endpoint="posts")
def posts_list():
    posts = db.session.query(Post).order_by(Post.published_at.desc())
    tags = db.session.query(Tag).all()

    # new_tags = (db.session.query(Tag, func.count(posts.c.post_id).label("posts_count")).
    #             join(posts).group_by(Post).order_by("posts_count DESC"))
    # new_tags = db.session.query(Tag, Tag.posts_number).order_by(Tag.posts_number.desc())

    return render_template(
        "posts_list.html",
        posts=posts,
        tags=tags,
    )


@habr_app.route("/refresh", endpoint="refresh")
def refresh_posts():
    fill_db_with_data()
    return redirect(url_for("habr_app.posts"))


@habr_app.route("/<int:post_id>/", endpoint="details")
def post_details(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    tags = db.session.query(Tag).all()

    if not post:
        return render_template("not_found.html", tags=tags)

    return render_template(
        "post_details.html",
        post=post,
        tags=tags,
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
