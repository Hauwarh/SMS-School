from flask import request
from flask_restx import Namespace, Resource, fields

course_namespace = Namespace('course', description='Namespace for course')