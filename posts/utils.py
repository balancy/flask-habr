from bs4 import BeautifulSoup
import requests
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from posts.models.database import db
from posts.models.habr_entities import Tag, Post, User, PostTagLink

HABR_URL = "https://habr.com/ru/news/"


def get_article_full_text(url):
    """Get full text of article.

    :param url: url of article
    :return: full text in html format
    """

    response = requests.get(url)
    response.raise_for_status()

    parsed_html = BeautifulSoup(response.text, "lxml")
    return parsed_html.select_one("#post-content-body")


def fetch_posts_from_habr():
    """Parse new posts from habrhabr.ru.

    :return: list of posts
    """

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
            "text": str(get_article_full_text(post_url)),
            "cover_image": image_tag["src"] if image_tag else None,
            "username": post.select_one(".post__meta .user-info").text.strip(),
            "tags": [elm.text for elm in post.select(
                ".post__hubs .inline-list__item_hub a"
            )]
        }
        news_set.append(record)

    return news_set


def handle_adding_db_record(db_record):
    """Handling adding record in DB.

    :param db_record: record in DB
    :return: db record id
    """

    db.session.add(db_record)
    try:
        db.session.commit()
        return db_record.id
    except IntegrityError:
        db.session.rollback()
        raise InternalServerError(f"Error adding {db_record}")


def create_or_get_user(username):
    """Gets existing or creates new user.

    :param username: user's username
    :return: user id
    """

    user = db.session.query(User).filter_by(username=username).first()
    if not user:
        user = User(username=username)
        handle_adding_db_record(user)
    return user.id


def create_or_get_post(user_id, title, description, text, cover_image):
    """Gets existing or creates new post.

    :param user_id: id of post author
    :param title: post title
    :param description: post description
    :param text: post full text
    :param cover_image: post cover image
    :return: post id
    """

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
    """Gets existing or creates new tag.

    :param title: tag title
    :return: tag id
    """

    tag = db.session.query(Tag).filter_by(title=title).first()
    if not tag:
        tag = Tag(title=title)
        handle_adding_db_record(tag)
    return tag.id


def create_or_get_post_tag_link(post_id, tag_id):
    """Gets existing or creates new post_tag_link.

    :param post_id: post id
    :param tag_id: tag id
    :return: post_tag_link id
    """

    post_tag_link = db.session.query(PostTagLink).filter_by(
        post_id=post_id, tag_id=tag_id
    ).first()

    if not post_tag_link:
        post_tag_link = PostTagLink(post_id=post_id, tag_id=tag_id)
        handle_adding_db_record(post_tag_link)
    return post_tag_link.id


def fill_db_with_data():
    """Populates DB with data.
    """

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
    """Fetch 10 most popular tags from DB.

    :return: popular tags
    """

    popular_tags = db.session.query(
        Tag, db.func.count(Post.id).label("count"),
    ).outerjoin(Post.tags).group_by(Tag.id).order_by(desc("count"))

    return popular_tags[:10]
