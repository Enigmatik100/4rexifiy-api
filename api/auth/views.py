import validators
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from werkzeug.exceptions import Conflict, BadRequest

from ..models.models import User
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash

auth_namespace = Namespace('auth', description="a namespace for authentication")

registration_model = auth_namespace.model(
    'User', {
        'firstname': fields.String(required=True, description="A firstname"),
        'lastname': fields.String(required=True, description="A lastname"),
        'email': fields.String(required=True, description="A email"),
        'password': fields.String(required=True, description="A password"),
    }
)

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'firstname': fields.String(required=True, description="A firstname"),
        'lastname': fields.String(required=True, description="A lastname"),
        'email': fields.String(required=True, description="An email"),
        'is_active': fields.Boolean(description="This shows that User is active"),
        'is_staff': fields.Boolean(description="This shows of use is staff")
    }

)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password")
    }
)


@auth_namespace.route('/register')
class Register(Resource):
    """
    Register user
    """

    @auth_namespace.marshal_with(user_model)
    @auth_namespace.expect(registration_model)
    def post(self):
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        # error_message = {}
        # if not firstname:
        #     error_message['firstname'] = 'firstname is required'
        # if not lastname:
        #     error_message['lastname'] = 'lastname is required'
        #
        # if len(password) < 8:
        #     error_message['password'] = "Password is to short"
        #
        # if not validators.email(email):
        #     error_message['password'] = "Email is not valid"
        # print(error_message)
        # if error_message:
        #     return error_message, HTTPStatus.BAD_REQUEST

        try:
            new_user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=generate_password_hash(password)
            )
            new_user.save()

            return new_user, HTTPStatus.CREATED
        except Exception as e:
            raise Conflict(f"User with email {data.get('email')} already exists")


@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_model)
    def post(self):
        """
        Generate  user's JWToken
        """

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            response = {'access_token': access_token, 'refresh_token': refresh_token}
            return response, HTTPStatus.OK
        raise BadRequest('Invalid username or password')


@auth_namespace.route('/refresh')
class Refresh(Resource):
    """
    Refresh user token
    """

    @jwt_required(refresh=True)
    def post(self):
        email = get_jwt_identity()
        access_token = create_access_token(identity=email)
        return {'access_token': access_token}, HTTPStatus.OK
