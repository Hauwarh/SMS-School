from ..utils import db
from enum import Enum


class UserType(Enum):
    ADMIN = 'admin'
    STUDENT = "student"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    first_name =db.Column(db.String(45), nullable=False)
    last_name =db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    user_type = db.Column(db.Enum(UserType), default=UserType.ADMIN)


    def __repr__(self):
        return f"<User {self.email}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)