# utf-8
# Python Imports
import datetime

# Framework Imports
from flask import render_template, flash, redirect, url_for, request
from flask.ext.security import login_required
from flask.ext.login import current_user

# App Imports
from app import db
from config import ADMIN_PER_PAGE
from app.admin import admin
from app.admin import forms
from app.models import Comment
from app.admin.helpers import *
from app.services.objects import *
from app.services.tags import *


# Views
@admin.route('/')
@login_required
def index():
    if current_user.first_name is None:
        flash('Please, setup your profile!')
        return redirect(url_for('admin.edit_profile'))
    return render_template('admin/index.html')


# Flask-Security edit extended-profile
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
    query = get_objects()
    pagination = paginate(query, ADMIN_PER_PAGE)
    return render_template('admin/object/all.html',
                           objects=pagination.items,
                           now=datetime.datetime.now(),
                           count=query.count(),
                           pagination=pagination)


@admin.route('/objects/posts')
@login_required
def posts():
    label_ob = 'Post'
    query = get_objects(label_ob.lower())
    pagination = paginate(query, ADMIN_PER_PAGE)
    return render_template('admin/object/category.html',
                           objects=pagination.items,
                           now=datetime.datetime.now(),
                           count=query.count(),
                           pagination=pagination,
                           label=label_ob)


@admin.route('/objects/links')
@login_required
def links():
    label_ob = 'Link'
    query = get_objects(label_ob.lower())
    pagination = paginate(query, ADMIN_PER_PAGE)
    return render_template('admin/object/category.html',
                           objects=pagination.items,
                           now=datetime.datetime.now(),
                           count=query.count(),
                           pagination=pagination,
                           label=label_ob)


@admin.route('/objects/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = forms.Post()
    if form.validate_on_submit():
        create_objects('post',
                       form.title.data,
                       slugify(form.title.data),
                       form.headline.data,
                       form.body.data,
                       current_user,
                       get_tags(form.tags.data))
        flash('Your post has been created.')
        return redirect(url_for('admin.all'))
    return render_template('admin/object/new_post.html',
                           form=form)


@admin.route('/objects/links/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = forms.Link()
    if form.validate_on_submit():
        create_objects('link',
                       form.title.data,
                       slugify(form.title.data),
                       '',
                       form.link.data,
                       current_user,
                       get_tags(form.tags.data))
        flash('Your link has been created.')
        return redirect(url_for('admin.all'))
    return render_template('admin/object/new_link.html',
                           form=form)


@admin.route('/objects/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = forms.Post()
    object_info = get_object_by_id(id)
    if object_info.object_type == 'link':
        return redirect(url_for('admin.links'))
    else:
        if form.validate_on_submit():
            object_info.body = form.body.data
            object_info.title = form.title.data
            object_info.slug_title = slugify(form.title.data)
            object_info.headline = form.headline.data
            object_info.last_update = datetime.datetime.now()
            object_info.tags = get_tags(form.tags.data)
            db.session.add(object_info)
            db.session.commit()
            flash('Your post has been updated.')
            return redirect(url_for('admin.all'))
    tags = []
    for tag in object_info.tags:
        tags.append(tag.name)
    form.body.data = object_info.body
    form.tags.data = " ".join(tags)
    form.title.data = object_info.title
    form.headline.data = object_info.headline
    return render_template('admin/object/edit_post.html',
                           form=form)


@admin.route('/objects/links/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_link(id):
    form = forms.Link()
    object_info = get_object_by_id(id)
    if object_info.object_type == 'post':
        flash('This object is a Post, select this object bellow')
        return redirect(url_for('admin.posts'))
    else:
        if form.validate_on_submit():
            object_info.body = form.link.data
            object_info.title = form.title.data
            object_info.slug_title = slugify(form.title.data)
            object_info.last_update = datetime.datetime.now()
            object_info.tags = get_tags(form.tags.data)
            object_info.author = current_user
            db.session.add(object_info)
            db.session.commit()
            flash('Your link has been updated')
            return redirect(url_for('admin.all'))
    tags = []
    for tag in object_info.tags:
        tags.append(tag.name)
    form.link.data = object_info.body
    form.tags.data = " ".join(tags)
    form.title.data = object_info.title
    return render_template('admin/object/edit_link.html',
                           form=form)


@admin.route('/objects/visible/<int:id>')
@login_required
def turn_visible(id):
    process = enable_disable_objects(id)
    flash(process)
    return redirect(url_for('admin.all'))


@admin.route('/objects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    form = forms.Delete()
    query = get_object_by_id(id)
    if form.validate_on_submit():
        db.session.delete(query)
        db.session.commit()
        flash('Your object has been deleted')
        return redirect(url_for('admin.all'))
    return render_template('admin/object/delete.html',
                           object=query,
                           form=form,
                           now=datetime.datetime.now())


@admin.route('/tags')
@login_required
def all_tags():
    query = get_all_tags()
    pagination = paginate(query, ADMIN_PER_PAGE)
    return render_template('admin/tag/all.html',
                           tags=pagination.items,
                           count=query.count(),
                           now=datetime.datetime.now(),
                           pagination=pagination)


@admin.route('/tags/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tag(id):
    form = forms.Tag()
    tag = get_tag_by_id(id)
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
    form = forms.Delete()
    tag = get_tag_by_id(id)
    objects = get_objects_by_tag(tag)
    if form.validate_on_submit():
        db.session.delete(tag)
        db.session.commit()
        flash('Your tag has been deleted')
        return redirect(url_for('admin.all_tags'))
    return render_template('admin/tag/delete.html',
                           tag=tag,
                           objects=objects,
                           form=form,
                           now=datetime.datetime.now())


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


@admin.route('/comments/delete/<int:id>', methods=['GET', 'POST'])
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
