from flask import Flask
from werkzeug.exceptions import NotFound, MethodNotAllowed

from .auth.views import auth_namespace
from .post.views import post_namespace
from .user.views import user_namespace

from flask_restx import Api
from .config.config import config_dict
from .models.models import User, Post, Comment

from .utils import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


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

    api.add_namespace(user_namespace, path='')
    api.add_namespace(post_namespace, path='/posts')
    api.add_namespace(auth_namespace, path='/auth')

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

    return app
