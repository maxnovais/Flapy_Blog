# utf-8
# Python imports
import datetime

# Framework imports
from flask import render_template, url_for, redirect, flash, request

# App imports
from app.main import main
from app import db
from app.main import forms
from app.main.helpers import paginate
from app.models import Object, Tag, Comment, User
from app.services.objects import *
from app.services.tags import *
from config import GUEST_PER_PAGE


# Views
@main.route('/')
def index():
    links = get_objects('link', True)
    posts = get_objects('post', True)
    tags = get_all_tags()
    form = forms.Search()
    comments = Comment.query.order_by(Comment.created_on.desc()).filter_by(enabled=True)
    return render_template('index.html',
                           now=datetime.datetime.now(),
                           links=links,
                           posts=posts,
                           tags=tags,
                           comments=comments,
                           form=form)


@main.route('/search', methods=['POST'])
def search():
    form = forms.Search()
    if not form.validate_on_submit():
        flash('Sua busca deve ter ao menos 3 caracteres.')
        return redirect(url_for('main.index'))
    string = form.string.data
    links = search_items(string, 'link', True)
    posts = search_items(string, 'post', True)
    tags = search_tags(string)
    return render_template('main/search.html',
                           string=string,
                           links=links,
                           posts=posts,
                           tags=tags)


@main.route('/posts')
def posts():
    query = get_objects('post', True)
    pagination = paginate(query, GUEST_PER_PAGE)
    return render_template('main/objects.html',
                           tags=get_all_tags(),
                           now=datetime.datetime.now(),
                           objects=pagination.items,
                           pagination=pagination,
                           count=query.count(),
                           label='Posts')


@main.route('/links')
def links():
    query = get_objects('link', True)
    pagination = paginate(query, GUEST_PER_PAGE)
    return render_template('main/objects.html',
                           tags=get_all_tags(),
                           now=datetime.datetime.now(),
                           objects=pagination.items,
                           pagination=pagination,
                           count=query.count(),
                           label='Links')


@main.route('/tags')
def tags():
    return render_template('main/tags.html',
                           tags=get_all_tags())


@main.route('/tag/<int:id>')
def tag(id):
    tag = get_tag_by_id(id)
    query = get_objects_by_tag(tag, True)
    pagination = paginate(query, GUEST_PER_PAGE)
    return render_template('main/tag.html',
                           id=id,
                           now=datetime.datetime.now(),
                           objects=pagination.items,
                           pagination=pagination,
                           label=tag.name)


@main.route('/about')
def about():
    query = User.query.get_or_404(1)
    return render_template('main/about.html', user=query)


@main.route('/comments')
def comments():
    now = datetime.datetime.now()
    query = Comment.query.order_by(Comment.created_on.desc()).filter_by(enabled=True)
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=GUEST_PER_PAGE, error_out=False)
    comments = pagination.items
    count = query.count()
    return render_template('main/comments.html', count=count, now=now, comments=comments, pagination=pagination)


@main.route('/object/<string>', methods=['GET', 'POST'])
def object(string):
    form = forms.NewComment()
    now = datetime.datetime.now()
    query = Object.query.filter_by(slug_title=string).first_or_404()
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
        flash('Seu comentario foi encaminhado, aguarde ser autorizado pela moderacao para ser publicado.')
        return redirect(url_for('main.object', string=query.slug_title))
    comments = query.comments.filter_by(enabled=True)
    return render_template('main/object.html', now=now, object=query, comments=comments, form=form)
