from flask import request
from flask_restx import Namespace, Resource, fields
from ..utils import db
from ..models.users import User, UserType
from ..models.courses import Course
from ..models.student import Student, student_course
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import Unauthorized, Conflict


course_namespace = Namespace('course', description='Namespace for course')

course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description="Course's ID"),
        'course_name': fields.String(description="Course's Name", required=True),
        'Tutor': fields.String(description="Course's Teacher", required=True),
        'credit_hours': fields.Integer(description="Course credit hour", required=True),
    }
)

student_course_model = course_namespace.model(
    'StudentCourse', {
        'course_id': fields.Integer(description="Course's ID"),
        'student_id': fields.Integer(description="Student's User ID")
    } 
)

student_course_response = course_namespace.model(
    "student_course", {
        'id': fields.Integer(),
        'first_name': fields.String(required=True, description="A users firstname"),
        'last_name': fields.String(required=True, description="A users lastname"),
        'email': fields.String(required=True, description="An email")
     }
)

@course_namespace.route('/course')
class CourseRegisterGet(Resource):
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description="Create a new course. Authorized only for Admin",
        # responses={
        #     201: "Course Created"
        # }
    )
    @jwt_required()
    def post(self):

        """
            Create new courses by admin only.
        """

        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")

        data = request.get_json()

        course_name = data.get("Course_name")

        course = Course.query.filter_by(course_name=course_name).first()
        
        if course is not None:
            raise Conflict(f"Course with name {course_name} already exists")


        new_course = Course(
            course_name = data.get("course_name"),
            Tutor = data.get("Tutor"),
            credit_hours = data.get("credit hours")
        )

        new_course.save()

        return new_course, HTTPStatus.CREATED

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Get All Courses"
    )
    @jwt_required()
    def get(self):
        """
            Get All Courses
        """
        courses = Course.query.all()

        return courses, HTTPStatus.OK


@course_namespace.route('/course/<int:course_id>')
class RetrieveUpdateDelete(Resource):
    
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Retrieve a course by ID - Authorized only for Admin",
        params = {
            'course_id': "The course ID"
        }
    )
    @jwt_required()
    def get(self, course_id):
        """
            Retrieve a course by ID - Authorized only for Admin
        """
        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")
        
        course = Course.get_by_id(course_id)
        
        return course, HTTPStatus.OK
    
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Update a course by ID - Authorized only for Admin",
        params = {
            'course_id': "The course ID"
        }
    )
    @jwt_required()
    def put(self, course_id):
        """
            Update a course by ID 
        """
        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")
        
        course = Course.get_by_id(course_id)

        data = request.get_json()

        course.course_name = data.get('course_name')
        course.Tutor = data.get('Tutor')
        course.credit_hours = data.get('credit_hours')

        db.session.commit()

        return course, HTTPStatus.OK
    
    @course_namespace.doc(
        description = "Delete a Course by ID - Authorized only for Admin",
        params = {
            'course_id': "The course ID"
        }
    )
    @jwt_required()
    def delete(self, course_id):
        """
            Delete a course by ID 
        """
        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")
        
        course = Course.get_by_id(course_id)

        course.delete()

        return {"message": "Course Successfully Deleted"}, HTTPStatus.OK

@course_namespace.route('/course/<int:course_id>/students/<int:student_id>')
class EnrollRemoveStudentCourse(Resource):
    
    @course_namespace.doc(
        description = "Enroll a Student to a Course -  Authorized only for Admin",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @jwt_required()
    @course_namespace.expect(student_course_model)
    def post(self, course_id, student_id):
        """
            Enroll a Student to a Course -  Authorized only for Admin
        """
        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")

        courses = Course.get_by_id(course_id)
        student = Student.get_by_id(student_id)

        if student is None:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND

        if courses is None:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND

        student.course.append(courses)

        db.session.add(student)
        db.session.commit()

        return {"message": f"{student.first_name} {student.last_name} has successfully been enrolled to {courses.course_name}"}, HTTPStatus.OK

    
    @course_namespace.doc(
        description = "Remove a Student to a Course -  Authorized only for Admin",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @jwt_required()
    @course_namespace.expect(student_course_model)
    def delete(self, course_id, student_id):
        """
            Remove a Student from a Course -  Authorized only for Admin
        """
        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")

        courses = Course.get_by_id(course_id)
        student = Student.get_by_id(student_id)

        if student is None:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND

        if courses is None:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND

        student.course.remove(courses)

        db.session.add(student)
        db.session.commit()

        return {"message":"course enrolled removed"}



@course_namespace.route('/<int:course_id>/students')
class GetAllStudentsInCourse(Resource):

    @course_namespace.doc(
        description = "Get All Students registered for a Course - Authorized only for admin",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @jwt_required()
    @course_namespace.marshal_with(student_course_response)
    def get(self, course_id):
        """
            Get All Students registered for a Course - Authorized only for admin
        """
        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")

        course = Course.get_by_id(course_id)

        students = course.students

        return students




