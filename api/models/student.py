from ..utils import db
from .users import User



student_course = db.Table('student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)


class Student(User):
    __tablename__='students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    course = db.relationship('Course', secondary='student_course', backref=db.backref('student', lazy='dynamic'))
    grade = db.relationship('Grade', backref='student_grade', lazy=True)



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
