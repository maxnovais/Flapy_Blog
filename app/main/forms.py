from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, BooleanField, SelectField
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import Required, Length


class NewComment(Form):
    name = TextField('Nome', [Required(), Length(1, 255)])
    email = TextField('Email', [Required(), Length(1, 255)])
    publish_email = BooleanField('Publicar Email')
    body = PageDownField('Comentario', [Required()])
    submit = SubmitField('Enviar')


class Search(Form):
    string = TextField('String', [Required(), Length(3, 255)])
    submit = SubmitField('Buscar')