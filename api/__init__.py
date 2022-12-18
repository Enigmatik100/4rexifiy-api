import logging
from logging.handlers import RotatingFileHandler

from click import echo
from flask import Flask
from flask.logging import default_handler
from werkzeug.exceptions import NotFound, MethodNotAllowed

from .auth.views import auth_namespace
from .comment.views import comment_namespace
from .post.views import post_namespace
from .user.views import user_namespace

from flask_restx import Api
from .config.config import config_dict
from .models.models import User, Post, Comment

from .utils import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

import sqlalchemy as sa


def configure_logging(app):
    # Logging Configuration
    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = RotatingFileHandler('instance/flask-user-management.log',
                                           maxBytes=16384,
                                           backupCount=20)
        file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    app.logger.info('Starting the Flask User Management App...')


def create_app(config=config_dict['prod']):
    app = Flask(__name__)

    app.config.from_object(config)
    authorizations = {
        "Bearer Auth": {
            'type': "apiKey",
            'in': 'header',
            'name': "Authorization",
            'description': "Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }
    api = Api(app,
              title="4rexify API",
              description="A REST API for 4rexify",
              authorizations=authorizations,
              security="Bearer Auth"
              )
    api.add_namespace(comment_namespace, path='')
    api.add_namespace(user_namespace, path='')
    api.add_namespace(post_namespace, path='/posts')
    api.add_namespace(auth_namespace, path='/auth')

    configure_logging(app)
    # register_cli_commands(app)

    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method not allowed"}, 405

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Post': Post,
            'Comment': Comment
        }

    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')

    return app


def register_cli_commands(app):
    @app.cli.command('init_db')
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo('Initialized the database!')
