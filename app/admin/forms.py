from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import TextField, SubmitField
from wtforms.validators import Required, Length


class EditProfileForm(Form):
    first_name = TextField('First Name', [Required(), Length(1, 255)])
    last_name = TextField('Last Name', [Required(), Length(1, 255)])
    location = TextField('Location', [Length(0, 255)])
    about = PageDownField('About')
    submit = SubmitField('Submit')


class Post(Form):
    title = TextField('Title', [Required(), Length(1, 100)])
    tags = TextField('Tags', [Length(0, 255)])
    headline = TextField('Headline', [Required(), Length(1, 255)])
    body = PageDownField('Post', [Required()])
    submit = SubmitField('Submit')


class Link(Form):
    title = TextField('Title', [Required(), Length(1, 100)])
    tags = TextField('Tags', [Length(0, 255)])
    link = TextField('Link', [Required()])
    submit = SubmitField('Submit')


class Tag(Form):
    name = TextField('Title', [Required(), Length(1, 30)])
    submit = SubmitField('Submit')


class Delete(Form):
    submit = SubmitField('Yes')
