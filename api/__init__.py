from flask import Flask
from flask_restx import Api 
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .courses.views import course_namespace
from .auth.views import auth_namespace
from .students.views import student_namespace
from .config.config import config_dict
from .utils import db
from .models.courses import Course
from .models.users import User
from .models.student import Student, student_course
from .models.grade import Grade
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)





    # authorizations = {
    #     "Bearer Auth": {
    #         "type": "apiKey",
    #         "in": "header",
    #         "name": "Authorization",
    #         "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
    #     }
    # }



    api = Api(
        app,
        title='Student Management API',
        description='A student management REST API service',
        # authorizations=authorizations,
        # security='Bearer Auth'
        )

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(course_namespace)
    api.add_namespace(student_namespace)


    # @api.errorhandler(NotFound)
    # def not_found(error):
    #     return{"error": "Not Found"},404

    # @api.errorhandler(MethodNotAllowed)
    # def method_not_allowed(error):
    #     return{"error": "Method Not Allowed"},404



    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Course': Course,
            'Student': Student,
            'Grade': Grade,
            'student_course': student_course
        }

    return app
