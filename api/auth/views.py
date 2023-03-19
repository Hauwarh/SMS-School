from flask import request, jsonify
from functools import wraps
from flask_restx import Namespace, Resource, fields
from ..models.users import User, UserType
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt

auth_namespace = Namespace('auth', description='Namespace for Authentication')

signup_model = auth_namespace.model(
    'Signup', {
        'first_name': fields.String(required=True, description="A users firstname"),
        'last_name': fields.String(required=True, description="A users lastname"),
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password"),
        'user_type': fields.String(description='Current User Type', required=True,
            enum = ['ADMIN', 'STUDENT'])
    }
)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password")
    }
)

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'first_name': fields.String(required=True, description="A users firstname"),
        'last_name': fields.String(required=True, description="A users lastname"),
        'email': fields.String(required=True, description="An email"),
        'password_hash': fields.String(required=True, description="A password"),
        'is_admin': fields.Boolean(description="This shows that if a User is an admin"),
        'user_type': fields.String(description='Current User Type', required=True,
            enum = ['ADMIN', 'STUDENT'])
    }
)



@auth_namespace.route('/signup')
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
            Register a User 
        """

        data = request.get_json()

        new_user = User(
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password')),
            user_type = data.get(UserType.ADMIN)
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token
        """

        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Generate Refresh Token
        """
        email = get_jwt_identity()

        access_token = create_access_token(identity=email)

        return {'access_token': access_token}, HTTPStatus.OK

# @auth_namespace.route('/admin-only')
# @jwt_required
# def admin_only():
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             verify_jwt_in_request()
#             claims = get_jwt()
#             if claims ["UserType.dmin"]:
#                 return fn(*args, **kwargs)
#             else:
#                 return jsonify(msg="Admins only!"), 403

#         return decorator

#     return wrapper