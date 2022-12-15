import datetime
from http import HTTPStatus

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields

from ..models.models import User, Post, Comment
from ..utils import db

comment_namespace = Namespace('comments', description="a namespace for the comment")

comment_model = comment_namespace.model(
    'Comment', {
        'id': fields.Integer(),
        'content': fields.String(required=True, description="A firstname"),
        'created_at': fields.DateTime(required=True, description="publish date"),
        'updated_at': fields.DateTime(required=True, description="updated date"),
        'post_id': fields.Integer(),
        'user_id': fields.Integer()
    }

)

post_comment_model = comment_namespace.model(
    'Comment', {
        'content': fields.String(required=True, description="A firstname"),
    }
)


@comment_namespace.route('/posts/<int:post_id>/comments/')
class AddCommentToOrGetPost(Resource):

    @comment_namespace.marshal_with(comment_model)
    @comment_namespace.expect(post_comment_model)
    @jwt_required()
    @comment_namespace.doc(
        description="Add comment to a specific post"
    )
    def post(self, post_id):
        """
        add comment to specific post
        """
        data = request.get_json()
        post = Post.query.get_or_404(post_id)
        comment = Comment(
            content=data.get('content')
        )

        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()
        comment.user_id = current_user.id

        post.comments.append(comment)

        db.session.commit()

        return comment, HTTPStatus.CREATED

    @comment_namespace.marshal_with(comment_model)
    @comment_namespace.doc(
        description="Retrieve all comment for a specific post"
    )
    def get(self, post_id):
        """
        Get all comments for specific post
        """
        post = Post.query.get_or_404(post_id)
        comments = post.comments
        return comments, HTTPStatus.OK


@comment_namespace.route('/posts/<int:post_id>/comments/<int:comment_id>')
class DeleteOrUpdateComment(Resource):

    @comment_namespace.marshal_with(comment_model)
    @comment_namespace.expect(post_comment_model)
    @jwt_required()
    @comment_namespace.doc(
        description="Add comment to a specific post"
    )
    def patch(self, post_id, comment_id):
        """
        update comment to specific post
        """
        data = request.get_json()
        post = Post.query.get_or_404(post_id)
        comment = Comment.query.get_or_404(comment_id)

        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()
        comment.user_id = current_user.id
        comment.content = data.get('content')
        comment.updated_at = datetime.datetime.now()

        db.session.commit()

        return comment, HTTPStatus.CREATED

    @jwt_required()
    @comment_namespace.doc(
        description="Add comment to a specific post"
    )
    @comment_namespace.marshal_with(comment_model)
    def delete(self, post_id, comment_id):
        """
        update comment to specific post
        """
        post = Post.query.get_or_404(post_id)
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return comment, HTTPStatus.OK
