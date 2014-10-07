import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    #Security configs
    SECURITY_PASSWORD_HASH = os.environ.get('PASS_HASH') or 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = os.environ.get('PASS_SALT') or 'abc'
    SECURITY_EMAIL_SENDER = 'Flapy Security <flapy-security@admin-example.com>'

    #Security customs URLs
    SECURITY_URL_PREFIX = '/auth'
    SECURITY_POST_LOGIN_VIEW = '/admin'
    SECURITY_POST_LOGOUT_VIEW = '/'

    #Security permissions
    SECURITY_REGISTERABLE = 'true'
    SECURITY_CHANGEABLE = 'true'
    SECURITY_TRACKABLE = 'true'

    #Mail config
    #Initial config set up using Google Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'username@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'

    #Blog Settings
    COMMENTS_INITIAL_ENABLED= True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
