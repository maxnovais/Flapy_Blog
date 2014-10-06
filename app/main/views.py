from . import main
from flask import render_template, url_for, redirect, flash
from .. import db
from . import forms
from ..models import Object, Tag, Comment, User
import datetime


# Views
@main.route('/')
def index():
    now = datetime.datetime.now()
    links = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='link', enabled=True)
    posts = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='post', enabled=True)
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


@main.route('/posts')
def posts():
    now = datetime.datetime.now()
    query = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='post', enabled=True)
    return render_template('main/objects.html', now=now, objects=query, label="Posts")


@main.route('/links')
def links():
    now = datetime.datetime.now()
    query = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='link', enabled=True)
    return render_template('main/objects.html', now=now, objects=query, label="Links")


@main.route('/tags')
def tags():
    query = Tag.query.all()
    return render_template('main/tags.html', tags=query)


@main.route('/tag/<int:id>')
def tag(id):
    now = datetime.datetime.now()
    tag = Tag.query.get_or_404(id)
    query = Object.query.filter(Object.tags.contains(tag))
    return render_template('main/tag.html', now=now, objects=query, label=tag.name)




@main.route('/comments')
def comments():
    now = datetime.datetime.now()
    query = Comment.query.order_by(Comment.created_on.desc()).filter_by(disabled=False)
    comments = query.all()
    return render_template('main/comments.html', now=now, comments=comments, count=query.count())


@main.route('/about')
def about():
    query = User.query.get_or_404(1)
    return render_template('main/about.html', user=query)


@main.route('/object/<int:id>', methods=['GET', 'POST'])
def object(id):
    form = forms.NewComment()
    now = datetime.datetime.now()
    query = Object.query.get_or_404(id)
    if query.enabled is False:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        new_comment = Comment(
            name=form.name.data,
            email=form.email.data,
            body=form.body.data,
            object_id=query
            )
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been created.')
        return redirect(url_for('main.object', id=query.id))
    comments = query.comments
    return render_template('main/object.html', now=now, object=query, comments=comments, form=form)
