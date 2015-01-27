# utf-8
# App imports
from app.models import Object


def Get_Objects(type_item=None, enabled=None):
    query = Object.query.order_by(Object.created_on.desc())
    if type_item:
        query = query.filter_by(object_type=type_item)
    if enabled:
        query = query.filter_by(enabled=enabled)
    return query
