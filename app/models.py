from datetime import datetime
from . import db
from flask.ext.login import UserMixin
from config import Config
from markdown import markdown
import bleach

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role %r>' % self.name


class TrueSelf(object):

    @property
    def self(self):
        """If self was pointed to by a proxy, present the true self.

        E.g. if self was returned by current_user, which is a proxy,
        we actually want to have the actual User object on an entry,
        not the one varying with each request.

        Also vital for storing into DB.
        """
        return self


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    about = db.Column(db.String)
    about_html = db.Column(db.String)
    location = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(40))
    current_login_ip = db.Column(db.String(40))
    login_count = db.Column(db.Integer())
    objects = db.relationship('Object', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.email

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                                'h1', 'h2', 'h3', 'p']
        target.about_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(User.about, 'set', User.on_changed_body)


objects_tags = db.Table(
    'object_tags',
    db.Column('object_id', db.Integer, db.ForeignKey('object.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    created_on = db.Column(db.DateTime, index=True, default=datetime.now)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.name


class Object(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    object_type = db.Column(db.String(30))
    title = db.Column(db.String(100))
    headline = db.Column(db.String(255))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    created_on = db.Column(db.DateTime, index=True, default=datetime.now)
    last_update = db.Column(db.DateTime, index=True)
    enabled = db.Column(db.Boolean, default=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='object', lazy='dynamic')
    tags = db.relationship('Tag', secondary=objects_tags,
                            backref=db.backref('object', lazy='dynamic'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                                'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Page %r, Tags %r>' % (self.title, self.tags)


db.event.listen(Object.body, 'set', Object.on_changed_body)


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    publish_email = db.Column(db.Boolean)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    created_on = db.Column(db.DateTime, index=True, default=datetime.now)
    enabled = db.Column(db.Boolean, default=Config.COMMENTS_INITIAL_ENABLED)
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.name)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'b', 'blockquote', 'code', 'strong', 'i']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)
