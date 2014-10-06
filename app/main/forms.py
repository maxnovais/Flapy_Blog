from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, BooleanField
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import Required, Length


class NewComment(Form):
    name = TextField('Name', [Required(), Length(1, 255)])
    email = TextField('Email', [Required(), Length(1, 255)])
    body = PageDownField('Body', [Required()])
    submit = SubmitField('Submit')
