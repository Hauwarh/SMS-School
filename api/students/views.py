from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User, UserType
from ..models.student import Student
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from http import HTTPStatus
from easy_password_generator import PassGen
from werkzeug.exceptions import Unauthorized, Conflict
 

student_namespace = Namespace('student', description='Namespace for student')


passwordGenerator = PassGen()

student_signup_request = student_namespace.model(
    "student_Signup", {
        'first_name': fields.String(required=True, description="A users firstname"),
        'last_name': fields.String(required=True, description="A users lastname"),
        'email': fields.String(required=True, description="An email"),
    }
)

student_signup_response = student_namespace.model(
    "Student", {
        'user_id': fields.Integer(),
        'password':  fields.String(required=True, description='User type')
    }
)

@student_namespace.route('/student')
class StudentGetRegister(Resource):
    @student_namespace.expect(student_signup_request)
    @student_namespace.marshal_with(student_signup_response)
    @student_namespace.doc(
        description="Create a new student. Authorized only for Admin",
        responses={
            201: "Password for created student"
        }
    )
    @jwt_required()
    def post(self):
        """Signup new students
        """
        logged_email=get_jwt_identity()

        data = request.get_json()

        password = passwordGenerator.generate()

        new_email= data.get('email')
        first_name = data.get('first_name')
        last_name= data.get('last_name')

        loggedin_user = User.query.filter_by(email=logged_email).first()

        if loggedin_user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")
        
        new_user = User.query.filter_by(email=new_email).first()

        if new_user is not None:
            raise Conflict(f"User with email {new_email} already exists")

        new_student = Student(
            email=new_email,
            first_name=first_name,
            last_name=last_name,
            password_hash=generate_password_hash(password),
            user_type=UserType.STUDENT
        )

        new_student.save()

        return {"password": password}, HTTPStatus.CREATED


    def get(self):
        """Retrive all students
        """
        pass

@student_namespace.route('/student/')
class StudentRetriveUpdateDelete(Resource):
    def get(self):
        pass