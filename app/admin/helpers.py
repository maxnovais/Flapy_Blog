# utf-8
# Python Imports
import re
from unidecode import unidecode

# Framework Imports
from flask import request

# App Imports
from app.models import Tag, User
from app import db


def get_tags(form_tags_data):
    string_tags = form_tags_data
    string_tags = string_tags.split(' ')
    tag_objects = []
    for strtag in string_tags:
        exists = Tag.query.filter_by(name=strtag).first()
        if not exists:
            exists = Tag(name=strtag)
            db.session.add(exists)
            db.session.commit()
        tag_objects.append(exists)
    return tag_objects


def get_current_user(c_user):
    current_id = int(c_user)
    user = User.query.filter_by(id=current_id).first()
    return user


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return unicode(delim.join(result))


def paginate(query, unity):
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=unity, error_out=False)
    return pagination
