from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User, UserType
from ..models.student import Student
from http import HTTPStatus
from ..utils import db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import  get_jwt_identity, jwt_required
from http import HTTPStatus
from easy_password_generator import PassGen
from werkzeug.exceptions import Unauthorized, Conflict
 

student_namespace = Namespace('student', description='Namespace for student')


passwordGenerator = PassGen()

student_signup_request = student_namespace.model(
    "student_signup", {
        'first_name': fields.String(required=True, description="A users firstname"),
        'last_name': fields.String(required=True, description="A users lastname"),
        'email': fields.String(required=True, description="An email"),
    }
)

student_model = student_namespace.model(
    "student_model", {
        'id': fields.Integer(),
        'first_name': fields.String(required=True, description="A users firstname"),
        'last_name': fields.String(required=True, description="A users lastname"),
        'email': fields.String(required=True, description="An email"),
        'password_hash': fields.String(required=True, description="A password"),
        'user_type': fields.String(description='User type', required=True,
            enum = ['ADMIN', 'STUDENT'])

    }
)

course_model = student_namespace.model(
    'Course', {
        'id': fields.Integer(description="Course's ID"),
        'course_name': fields.String(description="Course's Name", required=True),
        'Tutor': fields.String(description="Course's Teacher", required=True),
        'credit_hours': fields.Integer(description="Course credit hour", required=True),
    }
)

student_signup_response = student_namespace.model(
    "Student", {
        'password': fields.String(required=True, description='Student password')
    }
)

@student_namespace.route('/student')
class StudentRegisterGet(Resource):
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
        """Signup new students and generate password for each student
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
        
        new_user = Student.query.filter_by(email=new_email).first()

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

        return {"password": password}, HTTPStatus.CREATED #return password generated

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description= 'Retrive all students'
    )
    @jwt_required()
    def get(self):
        """
        Retrive all students

        """

        logged_email=get_jwt_identity()

        loggedin_user = User.query.filter_by(email=logged_email).first()

        if loggedin_user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")

        students = Student.query.all()
        

        return students, HTTPStatus.OK

@student_namespace.route('/student/<int:student_id>')
class StudentRetriveUpdateDelete(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description= 'Retrive student by Id - Authorized only for Admin and Specific Student',
         params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def get(self,student_id):

        """
            Retrieve student by ID
            
        """

        currrent_user_email = get_jwt_identity()

        loggedin_user = User.query.filter_by(email=currrent_user_email).first()
        print('loggedin_user:', loggedin_user)

        if loggedin_user.user_type is UserType.ADMIN:
        
            student = Student.get_by_id(student_id)

            return student, HTTPStatus.OK


        elif loggedin_user.user_type is UserType.STUDENT:
        
            student = Student.query.filter_by(email=get_jwt_identity()).first()

            student = Student.get_by_id(student.id)

            return student, HTTPStatus.OK

        elif not student:
            return Unauthorized("No student found")

        raise Unauthorized("Unauthorized Request")

    
    @student_namespace.expect(student_signup_request)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description=' Update a Student by ID',
        params = {
            'student_id': 'A student ID'
        }
    )
    @jwt_required()
    def put(self, student_id):
        """
            Update a Student by ID
        """
        logged_email=get_jwt_identity()

        loggedin_user = User.query.filter_by(email=logged_email).first()

        if loggedin_user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")

        update_student= Student.get_by_id(student_id)

        data = student_namespace.payload

        update_student.first_name = data["first_name"]
        update_student.last_name = data["last_name"]
        update_student.email = data["email"] 

        db.session.commit()

        return update_student, HTTPStatus.OK

    
    @student_namespace.doc(
        description='Delete a student by ID',
        params = {
            'student_id': 'An ID for a particular student'
        }
    )    
    @jwt_required()
    def delete(self, student_id):
        """
            Delete a student by ID

        """
        logged_email=get_jwt_identity()

        loggedin_user = User.query.filter_by(email=logged_email).first()

        if loggedin_user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")

        student = Student.get_by_id(student_id)

        student.delete()

        return {"message" " Student deleted successfully"}, HTTPStatus.OK


@student_namespace.route('/<int:student_id>/courses')
class GetAllCourseStudents(Resource):

    @student_namespace.doc(
        description = "Get All courses registerd by a student - Authorized only for admin",
        params = {
            'student_id': "The student's ID"
        }
    )
    @jwt_required()
    @student_namespace.marshal_with(course_model)
    def get(self, student_id):
        """
            Get All courses registerd by a student - Authorized only for admin
        """
        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")

        student = Student.get_by_id(student_id)

        if student is None:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND

        courses = student.course

        if courses is None:
            return {'message': 'Student not enrolled in any course'}, HTTPStatus.NOT_FOUND

        return courses
       

