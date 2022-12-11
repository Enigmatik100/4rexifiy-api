from http import HTTPStatus

from flask_restx import Namespace, Resource, fields

from .. import post_namespace
from ..models.models import Post, User

user_namespace = Namespace('users', description="a namespace for the user")


@user_namespace.route('/<int:user_id>/posts/')
class PostGetCreate(Resource):

    def get(self, user_id):
        """
        Get all relative to specific user
        """

        user = User.get_by_id(user_id)
        posts = user.posts
        return posts, HTTPStatus.OK
