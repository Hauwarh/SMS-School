from ..utils import db
from .users import User

class Student(User):
    __tablename__='students'
    studentId = db.Column(db.Integer(), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # username = db.Column(db.String(45), nullable=False, unique=True)
    # email = db.Column(db.String(50), nullable=False, unique=True)


    def __repr__(self):
        return f"<Student{self.id}>"
            
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
