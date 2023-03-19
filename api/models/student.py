from ..utils import db
from .users import User

class Student(User):
    __tablename__='students'
    studentId = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # course = db.relationship('Course', secondary='student_course', lazy=True)
    # grade = db.relationship('Grade', backref='student_grade', lazy=True)
    # username = db.Column(db.String(45), nullable=False, unique=True)
    # first_name = db.Column(db.String(45), nullable=False)
    # last_name = db.Column(db.String(45), nullable=False)
    # email = db.Column(db.String(50), nullable=False, unique=True)

    # username = db.Column(db.String(45), nullable=False, unique=True)
    # email = db.Column(db.String(50), nullable=False, unique=True)


    def __repr__(self):
        return f"<Student{self.StudentId}>"
            
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
