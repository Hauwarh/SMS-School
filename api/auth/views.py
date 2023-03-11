from flask import request
from flask_restx import Namespace, Resource, fields

auth_namespace = Namespace('auth', description='Namespace for Authentication')