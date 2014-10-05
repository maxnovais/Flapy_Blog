from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from config import config


db = SQLAlchemy()
bootstrap = Bootstrap()
security = Security()
moment = Moment()
pagedown = PageDown()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    mail.init_app(app)

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

    return app
