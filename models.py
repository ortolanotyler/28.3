# SQLAlchemy models for a blogg application

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class Blogger(db.Model):
    """A blogger/user of the blogging platform."""

    __tablename__ = "bloggers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("BlogPost", backref="blogger", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return the full name of the blogger."""
        return f"{self.first_name} {self.last_name}"






class BlogPost(db.Model):
    """A blog post."""

    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    blogger_id = db.Column(db.Integer, db.ForeignKey('bloggers.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return a nicely-formatted date."""
        return self.created_at.strftime("%a %b %-d, %Y, %-I:%M %p")


class PostTag(db.Model):
    """A tag associated with a blog post."""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)








class Tag(db.Model):
    """A tag that can be added to blog posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'BlogPost',
        secondary="post_tags",
        backref="tags",
    )


def connect_to_database(app):
    """Connect the database to the provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)
