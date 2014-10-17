from ..models import Tag, User
import re
from unidecode import unidecode
from .. import db


def get_tags(form_tags_data):
    stringtags = form_tags_data
    stringtags = stringtags.split(' ')
    tagobjects = []
    for strtag in stringtags:
        exists = Tag.query.filter_by(name=strtag).first()
        if not exists:
            exists = Tag(name=strtag)
            db.session.add(exists)
            db.session.commit()
        tagobjects.append(exists)
    return tagobjects


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
