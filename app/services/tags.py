# utf-8
# App imports
from app.models import Tag


def get_all_tags():
    query = Tag.query.order_by(Tag.created_on.desc())
    return query


def get_tag_by_id(id):
    query = Tag.query.filter_by(id=id).first_or_404()
    return query


def search_tags(string):
    query = Tag.query.filter(Tag.name.contains(string))
    return query
