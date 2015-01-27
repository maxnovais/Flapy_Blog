# utf-8
# Python imports
import datetime

# App imports
from app import db
from app.models import Object


def get_objects(type_item=None, enabled=None):
    query = Object.query.order_by(Object.created_on.desc())
    if type_item:
        query = query.filter_by(object_type=type_item)
    if enabled:
        query = query.filter_by(enabled=enabled)
    return query


def get_object_by_id(id):
    query = Object.query.filter_by(id=id).first_or_404()
    return query


def get_objects_by_tag(tag):
    query = Object.query.filter(Object.tags.contains(tag)).all()
    return query


def create_objects(object_type, title, slug_title, headline, body, author, tags):
    object_info = Object(object_type=object_type,
                         title=title,
                         slug_title=slug_title,
                         headline=headline,
                         body=body,
                         author=author,
                         tags=tags)
    db.session.add(object_info)
    db.session.commit()


def enable_disable_objects(id):
    query = get_object_by_id(id)
    if query.enabled is True:
        query.enabled = False
        query.last_update = datetime.datetime.now()
        db.session.add(query)
        db.session.commit()
        message = 'Your object has disabled!'
    else:
        query.enabled = True
        query.last_update = datetime.datetime.now()
        db.session.add(query)
        db.session.commit()
        message = 'Your object has enabled!'
    return message
