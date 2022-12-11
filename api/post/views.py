import datetime
import os
from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ..utils import db
from ..models.models import User, Post
from ..config import config

post_namespace = Namespace('posts', description="a namespace for the post")
post_model = post_namespace.model(
    'Post', {
        'id': fields.Integer(),
        'title': fields.String(required=True, description="A firstname"),
        'created_at': fields.DateTime(required=True, description="publish date"),
        'updated_at': fields.DateTime(required=True, description="updated date"),
        'image_file': fields.String(required=True, description="A cover of post"),
        'content': fields.String(required=True, description="A content"),
        'summary': fields.String(required=True, description="A summary"),
    }

)

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', help="title of blog")
post_parser.add_argument('summary', help="summary of blog")
post_parser.add_argument('content', help="content of blog")
post_parser.add_argument('image_file', location='files', type=FileStorage, required=True)


@post_namespace.route('/')
class GetAllPost(Resource):

    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="Retrieve all posts"
    )
    def get(self):
        """
        Get all posts
        """
        posts = Post.query.all()
        return posts, HTTPStatus.OK

    @jwt_required()
    @post_namespace.expect(post_parser)
    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="Create a post"
    )
    def post(self):
        """
        Create a post
        """
        # TODO find the way to serve static file

        email = get_jwt_identity()
        current_user = User.query.filter_by(email=email).first()

        data = post_parser.parse_args()
        image_file = data['image_file']  # This is FileStorage instance
        secured_filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(config.UPLOAD_FOLDER, secured_filename))

        post = Post(
            title=data.get('title'),
            content=data.get('content'),
            summary=data.get('summary'),
            image_file=config.UPLOAD_FOLDER + '/' + secured_filename,
            created_at=datetime.datetime.now()
        )

        post.user_id = current_user.id
        post.save()
        return {
                   'id': post.id,
                   'title': post.title,
                   'content': post.content,
                   'summary': post.summary,
                   'image_file': post.image_file,
                   'created_at': post.created_at,
                   'updated_at': post.updated_at
               }, HTTPStatus.OK


@post_namespace.route('/<int:post_id>/')
class GetUpdateDeletePost(Resource):

    @post_namespace.marshal_with(post_model)
    @jwt_required()
    def get(self, post_id):
        """
        Retrieve post for specific user by id
        """
        post = Post.query.get_or_404(post_id)
        return post, HTTPStatus.OK

    @post_namespace.expect(post_model)
    @post_namespace.marshal_with(post_model)
    @jwt_required()
    def put(self, post_id):
        """
        Update post for specific user by id
        """
        db_post = Post.query.get_or_404(post_id)
        data = post_namespace.payload

        db_post.title = data.get('title')
        db_post.summary = data.get('summary')
        db_post.content = data.get('content')
        db_post.image_file = data.get('image_file')

        db.session.commit()

        return db_post, HTTPStatus.OK

    @post_namespace.marshal_with(post_model)
    @jwt_required()
    def delete(self, post_id):
        """
        delete post for specific user by id
        """

        db_post = Post.query.get_or_404(post_id)
        db.session.delete(db_post)
        db.session.commit()

        return db_post, HTTPStatus.NO_CONTENT
