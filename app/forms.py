from flask_security.forms import RegisterForm
from wtforms import TextField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email


class RegisterForm(RegisterForm):
    email = TextField('Email', [Required(), Length(1, 255), Email()])
    password = PasswordField('Password', [Required(), Length(6, 255)])
    password_confirm = PasswordField('Password Again', [Required(), Length(6, 255)])
    first_name = TextField('First Name', [Required(), Length(1, 255)])
    last_name = TextField('Last Name', [Required(), Length(1, 255)])
    location = TextField('Location', [Length(0, 255)])
    about = TextAreaField('About', [Length(0, 255)])
    submit = SubmitField('Submit')
