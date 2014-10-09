from . import main
from flask import render_template, url_for, redirect, flash, request
from .. import db
from . import forms
from ..models import Object, Tag, Comment, User
import datetime
from config import GUEST_PER_PAGE


# Views
@main.route('/')
def index():
    now = datetime.datetime.now()
    links = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='link', enabled=True)
    posts = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='post', enabled=True)
    tags = Tag.query.order_by(Tag.created_on.desc())
    comments = Comment.query.filter_by(enabled=True)
    form = forms.Search()
    return render_template(
        'index.html',
        now=now,
        links=links,
        posts=posts,
        tags=tags,
        comments=comments,
        form=form
        )


@main.route('/search', methods=['POST'])
def search():
    form = forms.Search()
    if not form.validate_on_submit():
        flash('Your search must be at least 3 characters.')
        return redirect(url_for('main.index'))
    string = form.string.data
    links = Object.query.filter(Object.title.contains(string)).filter_by(object_type='link', enabled=True)
    posts = Object.query.filter(Object.title.contains(string)).filter_by(object_type='post', enabled=True)
    tags = Tag.query.filter(Tag.name.contains(string))
    return render_template('main/search.html', string= string, links=links, posts=posts, tags=tags)



@main.route('/posts')
def posts():
    now = datetime.datetime.now()
    query = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='post', enabled=True)
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=GUEST_PER_PAGE, error_out=False)
    objects = pagination.items
    count = query.count()
    return render_template('main/objects.html', now=now, objects=objects, pagination=pagination, count=count, label="Posts")


@main.route('/links')
def links():
    now = datetime.datetime.now()
    query = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='link', enabled=True)
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=GUEST_PER_PAGE, error_out=False)
    objects = pagination.items
    count = query.count()
    return render_template('main/objects.html', now=now, objects=objects, pagination=pagination, count=count, label="Links")


@main.route('/tags')
def tags():
    query = Tag.query.all()
    return render_template('main/tags.html', tags=query)


@main.route('/tag/<int:id>')
def tag(id):
    now = datetime.datetime.now()
    tag = Tag.query.get_or_404(id)
    query = Object.query.filter(Object.tags.contains(tag)).filter_by(enabled=True)
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=GUEST_PER_PAGE, error_out=False)
    objects = pagination.items
    return render_template('main/tag.html', id=id, now=now, objects=objects, pagination=pagination, label=tag.name)




@main.route('/comments')
def comments():
    now = datetime.datetime.now()
    query = Comment.query.order_by(Comment.created_on.desc()).filter_by(enabled=True)
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=GUEST_PER_PAGE, error_out=False)
    comments = pagination.items
    count = query.count()
    return render_template('main/comments.html', count=count, now=now, comments=comments, pagination=pagination)


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
            publish_email=form.publish_email.data,
            object_id=query.id
            )
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been created.')
        return redirect(url_for('main.object', id=query.id))
    comments = query.comments.filter_by(enabled=True)
    return render_template('main/object.html', now=now, object=query, comments=comments, form=form)
