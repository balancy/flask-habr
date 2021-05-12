from bs4 import BeautifulSoup
import requests
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from posts.models.database import db
from posts.models.habr_entities import Tag, Post, User, PostTagLink

HABR_URL = "https://habr.com/ru/news/"


def get_full_text(url):
    response = requests.get(url)
    response.raise_for_status()

    parsed_html = BeautifulSoup(response.text, "lxml")
    return parsed_html.select_one("#post-content-body")


def fetch_posts_from_habr():
    response = requests.get(HABR_URL)
    response.raise_for_status()

    parsed_html = BeautifulSoup(response.text, "lxml")
    all_html_news = parsed_html.select(".posts_list .post")

    news_set = []
    for post in all_html_news:
        post_url = post.select_one(".post__title a")["href"]
        image_tag = post.select_one(".post__body-cover img")
        record = {
            "title": post.select_one(".post__title a").text,
            "description": post.select_one(".post__text").text,
            "text": str(get_full_text(post_url)),
            "cover_image": image_tag["src"] if image_tag else None,
            "username": post.select_one(".post__meta .user-info").text.strip(),
            "tags": [elm.text for elm in post.select(
                ".post__hubs .inline-list__item_hub a"
            )]
        }
        news_set.append(record)

    return news_set


def handle_adding_db_record(db_record):
    db.session.add(db_record)
    try:
        db.session.commit()
        return db_record.id
    except IntegrityError:
        db.session.rollback()
        raise InternalServerError(f"Error adding {db_record}")


def create_or_get_user(username):
    user = db.session.query(User).filter_by(username=username).first()
    if not user:
        user = User(username=username)
        handle_adding_db_record(user)
    return user.id


def create_or_get_post(user_id, title, description, text, cover_image):
    post = db.session.query(Post).filter_by(title=title).first()
    if not post:
        post = Post(
            title=title,
            description=description,
            text=text,
            user_id=user_id,
            cover_image=cover_image,
        )
        handle_adding_db_record(post)
    return post.id


def create_or_get_tag(title):
    tag = db.session.query(Tag).filter_by(title=title).first()
    if not tag:
        tag = Tag(title=title)
        handle_adding_db_record(tag)
    return tag.id


def create_or_get_post_tag_link(post_id, tag_id):
    post_tag_link = db.session.query(PostTagLink).filter_by(
        post_id=post_id, tag_id=tag_id
    ).first()

    if not post_tag_link:
        post_tag_link = PostTagLink(post_id=post_id, tag_id=tag_id)
        handle_adding_db_record(post_tag_link)
    return post_tag_link.id


def fill_db_with_data():
    posts = fetch_posts_from_habr()

    for post in posts:
        user_id = create_or_get_user(post["username"])
        post_id = create_or_get_post(
            user_id,
            post["title"],
            post["description"],
            post["text"],
            post["cover_image"],
        )
        for tag in post["tags"]:
            tag_id = create_or_get_tag(tag)
            create_or_get_post_tag_link(post_id, tag_id)


def get_popular_tags():
    popular_tags = db.session.query(
        Tag, db.func.count(Post.id).label("count"),
    ).outerjoin(Post.tags).group_by(Tag.id).order_by(desc("count"))

    return popular_tags[:10]
