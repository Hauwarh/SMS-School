from flask import jsonify
from functools import wraps
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_jwt_extended import JWTManager


# def admin_required():
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             verify_jwt_in_request()
#             claims = get_jwt()
#             if claims [""]:
#                 return fn(*args, **kwargs)
#             else:
#                 return jsonify(msg="Admins only!"), 403

#         return decorator

#     return wrapper