from flask import Flask
from flask_restx import Api
from .course .views import course_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.course import Order
from .models.users import User

