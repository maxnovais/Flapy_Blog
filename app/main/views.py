from . import main
from flask import render_template
from .. import db
from . import forms
from ..models import Object, Tag, Comment
import datetime


# Views
@main.route('/')
def index():
    now = datetime.datetime.now()
    links = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='link')
    posts = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='post')
    tags = Tag.query.order_by(Tag.created_on.desc())
    comments = Comment.query.order_by(Comment.created_on.desc())
    return render_template(
        'index.html',
        now=now,
        links=links,
        posts=posts,
        tags=tags,
        comments=comments
        )


@main.route('/object/')
def object_main():
    return render_template('main/object.html')


@main.route('/posts')
def posts():
    pass


@main.route('/links')
def links():
    pass


@main.route('/tags')
def tags():
    pass


@main.route('/tag/<int:id>')
def tag():
    pass


@main.route('/comments')
def comments():
    pass


@main.route('/about')
def about():
    pass


@main.route('/object/<int:id>')
def object(id):
    now = datetime.datetime.now()
    query = Object.query.filter_by(id=id).first_or_404()
    return render_template('main/object.html', now=now, object=query)
