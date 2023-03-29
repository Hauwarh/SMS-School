from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User, UserType
from ..models.student import Student
from ..models.courses import Course
from ..models.grade import Grade
from http import HTTPStatus
from ..utils import db
from flask_jwt_extended import  get_jwt_identity, jwt_required
from http import HTTPStatus
from werkzeug.exceptions import Unauthorized
 

grade_namespace = Namespace('grades', description='Namespace for grade')


grade_model = grade_namespace.model('Grade', {
    'student_id': fields.Integer(required=True),
    'course_id': fields.Integer(required=True),
    'grade': fields.String(required=True),
    'score': fields.Interger(required=True)
})


@grade_namespace.route('/grades/<int:student_id>')
class Grade(Resource):
    @grade_namespace.doc(
        description = "Retrieve a Student's Grades - Authorized for Admin or current student",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Retrieve a Student's Grades - Admins or Specific Student Only
        """
        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")
        
       # student = Student.get_by_id(student_id)
        student = Student.query.filter_by(id=student_id).first()
        if student is None:
                return {"message": "No Student found"}, HTTPStatus.NOT_FOUND
        
        grades = Grade.query.filter_by(student_id=id).all()
        if not grades:
            return { f"Grades for student {student.first_name} not found"}

        return grades


    @grade_namespace.doc(
        description = " Add a grade for a student in a course - Authorized for Admin ",
            param = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def post(self, student_id):
        """
           Add a grade for a student in a course - Authorized for Admin
        """
        current_user=get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        if user.user_type not in [UserType.ADMIN]:
            raise Unauthorized("Unauthorized Request")


        data = request.get_json()

        course_id = data.get(course_id)

        student = Student.get_by_id(student_id)
        course = Course.get_by_id(course_id)

        student_course = student_course.query.filter_by(student_id=student.id, course_id=course.id).first()
        if not student_course:
            return {"message": "Student or course not found"}, HTTPStatus.NOT_FOUND

        new_grade = Grade(
            student_id = student_id,
            course_id = data.get("course_id"),
            score = data.get("score"),
            grade = data.get('grade')
        )

        new_grade.save()

        return new_grade

grade_namespace.route('/grades/<int:grade_id>')
class UpdateDeleteGrade(Resource):

    @grade_namespace.expect(grade_model)
    @grade_namespace.doc(
        description = "Update a Grade - Authorised for admin only",
        params = {
            'grade_id': "The Grade's ID"
        }
    )
    @jwt_required()
    def put(self, grade_id):
        """
            Update a Grade - Admins Only
        """
        data = request.get_json()

        grade = Grade.get_by_id(grade_id)
        
        grade.score = data.get('score')
        grade.grade = data.get('score')
        
        grade.update()

        return grade, HTTPStatus.OK
    
    @grade_namespace.doc(
        description = "Delete a Grade - Authorized Only for admin",
        params = {
            'grade_id': "The Grade's ID"
        }
    )
    @jwt_required()
    def delete(self, grade_id):
        """
            Delete a Grade - Authorized Only for admin
        """
        grade = Grade.get_by_id(grade_id)
        
        grade.delete()

        return {"message": "Grade Successfully Deleted"}, HTTPStatus.OK


  # Calculate the GPA for a student based on their grades      
@grade_model.route('/students/<int:student_id>/gpa')
class StudentGPA(Resource):
    @grade_namespace.doc(
        description = "Calculate the GPA for a student based on their grades",
        params={
            'id': 'The student ID'
            }
    )
    @jwt_required()
    def get(self, id):
        """
        Calculate the GPA for a student based on their grades in each course using the standard 4.0 scale for calculating GPA
        """
        student = Student.query.filter_by(id=id).first()
        if student is None:
            return {'message': f"Student {id} not found"}

        grades = Grade.query.filter_by(student_id=id).all()
        total_credits = 0
        total_grade_points = 0

        for grade in grades:
            course = Course.query.filter_by(id=grade.course_id).first()

            credit_hours = course.credit_hours
            grade_points = grade.grade

            total_credits += credit_hours
            total_grade_points += grade_points * credit_hours

        gpa = total_grade_points / total_credits 

        return {'gpa': gpa}
                


