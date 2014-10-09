from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, BooleanField, SelectField
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import Required, Length


class NewComment(Form):
    name = TextField('Name', [Required(), Length(1, 255)])
    email = TextField('Email', [Required(), Length(1, 255)])
    publish_email = BooleanField('Publish Email')
    body = PageDownField('Body', [Required()])
    submit = SubmitField('Submit')


class Search(Form):
    string = TextField('Name', [Required(), Length(3, 255)])
    submit = SubmitField('Search')