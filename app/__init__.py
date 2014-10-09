from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
security = Security(app)
moment = Moment(app)
pagedown = PageDown(app)
mail = Mail(app)

from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(
    app,
    user_datastore,
    )

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')
