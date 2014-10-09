from flask import render_template, flash, redirect, url_for, request
from flask.ext.security import login_required
from flask.ext.login import current_user
from . import admin
from .. import db
from . import forms
from ..models import Object, Tag, Comment
from helpers import get_tags
import datetime
from config import ADMIN_PER_PAGE


# Views
@admin.route('/')
@login_required
def index():
    if current_user.first_name is None:
        flash('Please, setup your profile!')
        return redirect(url_for('admin.edit_profile'))
    return render_template('admin/index.html')


#Flask-Security edit extended-profile
@admin.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = forms.EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.location = form.location.data
        current_user.about = form.about.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.index'))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.location.data = current_user.location
    form.about.data = current_user.about
    return render_template('security/edit_profile.html', form=form)


@admin.route('/objects/')
@login_required
def all():
    now = datetime.datetime.now()
    page = request.args.get('page', 1, type=int)
    query = Object.query.order_by(Object.created_on.desc())
    pagination = query.paginate(page, per_page=ADMIN_PER_PAGE, error_out=False)
    objects = pagination.items
    count = query.count()
    return render_template('admin/object/all.html', objects=objects, now=now, count=count, pagination=pagination)


@admin.route('/objects/posts')
@login_required
def posts():
    label_ob = 'Post'
    now = datetime.datetime.now()
    query = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='post')
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=ADMIN_PER_PAGE, error_out=False)
    objects = pagination.items
    count = query.count()
    return render_template('admin/object/category.html', objects=objects, label=label_ob, now=now, count=count, pagination=pagination)


@admin.route('/objects/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = forms.NewPost()
    if form.validate_on_submit():
        post = Object(
            object_type='post',
            title=form.title.data,
            headline=form.headline.data,
            body=form.body.data,
            author=current_user,
            tags=get_tags(form.tags.data)
            )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.')
        return redirect(url_for('admin.all'))
    return render_template('admin/object/new_post.html', form=form,)


@admin.route('/objects/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = forms.EditPost()
    post = Object.query.filter_by(id=id).first_or_404()
    if post.object_type == 'link':
        flash('This object is a Hiperlink, select this object bellow')
        return redirect(url_for('admin.links'))
    else:
        if form.validate_on_submit():
            post.body = form.body.data
            post.title = form.title.data
            post.headline = form.headline.data
            post.last_update = datetime.datetime.now()
            post.tags = get_tags(form.tags.data)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been updated.')
            return redirect(url_for('admin.all'))
    tags = []
    for tag in post.tags:
        tags.append(tag.name)
    form.body.data = post.body
    form.tags.data = " ".join(tags)
    form.title.data = post.title
    form.headline.data = post.headline
    return render_template('admin/object/edit_post.html', form=form)


@admin.route('/objects/links')
@login_required
def links():
    label_ob = 'Link'
    now = datetime.datetime.now()
    query = Object.query.order_by(Object.created_on.desc()).filter_by(object_type='link')
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=ADMIN_PER_PAGE, error_out=False)
    objects = pagination.items
    count = query.count()
    return render_template('admin/object/category.html', objects=objects, label=label_ob, now=now, count=count, pagination=pagination)


@admin.route('/objects/links/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = forms.NewLink()
    if form.validate_on_submit():
        link = Object(
            object_type='link',
            title=form.title.data,
            body=form.link.data,
            author=current_user,
            tags=get_tags(form.tags.data)
            )
        db.session.add(link)
        db.session.commit()
        flash('Your link has been created')
        return redirect(url_for('admin.all'))
    return render_template('admin/object/new_link.html', form=form)


@admin.route('/objects/links/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_link(id):
    form = forms.EditLink()
    link = Object.query.filter_by(id=id).first_or_404()
    if link.object_type == 'post':
        flash('This object is a Post, select this object bellow')
        return redirect(url_for('admin.posts'))
    else:
        if form.validate_on_submit():
            link.body = form.link.data
            link.title = form.title.data
            link.last_update = datetime.datetime.now()
            link.tags = get_tags(form.tags.data)
            link.author = current_user
            db.session.add(link)
            db.session.commit()
            flash('Your link has been updated')
            return redirect(url_for('admin.all'))
    tags = []
    for tag in link.tags:
        tags.append(tag.name)
    form.link.data = link.body
    form.tags.data = " ".join(tags)
    form.title.data = link.title
    return render_template('admin/object/edit_link.html', form=form)


@admin.route('/objects/visible/<int:id>')
@login_required
def turn_visible(id):
    query = Object.query.filter_by(id=id).first_or_404()
    if query.enabled is True:
        query.enabled = False
        query.last_update = datetime.datetime.now()
        db.session.add(query)
        db.session.commit()
        flash('Your object turn in disabled')
    else:
        query.enabled = True
        query.last_update = datetime.datetime.now()
        db.session.add(query)
        db.session.commit()
        flash('Your object turn in enabled')
    return redirect(url_for('admin.all'))


@admin.route('/objects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    now = datetime.datetime.now()
    form = forms.Delete()
    query = Object.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        db.session.delete(query)
        db.session.commit()
        flash('Your object has been deleted')
        return redirect(url_for('admin.all'))
    return render_template('admin/object/delete.html', object=query, form=form, now=now)


@admin.route('/tags')
@login_required
def all_tags():
    query = Tag.query.order_by(Tag.created_on.desc())
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=ADMIN_PER_PAGE, error_out=False)
    tags = pagination.items
    count = query.count()
    now = datetime.datetime.now()
    return render_template('admin/tag/all.html', tags=tags, count=count, now=now, pagination=pagination)


@admin.route('/tags/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tag(id):
    form = forms.EditTag()
    tag = Tag.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()
        flash('Your link has been updated')
        return redirect(url_for('admin.all_tags'))
    form.name.data = tag.name
    return render_template('admin/tag/edit.html', tag=tag, form=form)


@admin.route('/tags/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_tag(id):
    now = datetime.datetime.now()
    form = forms.Delete()
    tag = Tag.query.filter_by(id=id).first_or_404()
    objects = Object.query.filter(Object.tags.contains(tag)).all()
    if form.validate_on_submit():
        db.session.delete(tag)
        db.session.commit()
        flash('Your tag has been deleted')
        return redirect(url_for('admin.all_tags'))
    return render_template('admin/tag/delete.html', tag=tag, objects=objects, form=form, now=now)


@admin.route('/comments')
@login_required
def all_comments():
    now = datetime.datetime.now()
    query = Comment.query.order_by(Comment.created_on.desc())
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=ADMIN_PER_PAGE, error_out=False)
    count = query.count()
    comments = pagination.items
    return render_template('admin/comment/all.html', now=now, count= count, comments=comments, pagination=pagination)


@admin.route('/comments/visible/<int:id>')
@login_required
def turn_visible_comment(id):
    query = Comment.query.filter_by(id=id).first_or_404()
    if query.enabled is True:
        query.enabled = False
        db.session.add(query)
        db.session.commit()
        flash('The comment is Disabled')
    else:
        query.enabled = True
        db.session.add(query)
        db.session.commit()
        flash('The comment is Enabled')
    return redirect(url_for('admin.all_comments'))


@admin.route('/comments/delete/<int:id>')
@login_required
def delete_comment(id):
    now = datetime.datetime.now()
    form = forms.Delete()
    query = Comment.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        db.session.delete(query)
        db.session.commit()
        flash('The comment has been deleted')
        return redirect(url_for('admin.all_comments'))
    return render_template('admin/comment/delete.html', comment=query, form=form, now=now)
