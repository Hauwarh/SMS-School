from ..utils import db

class Course(db.Model):
    __tablename__= 'courses'
    id =  db.Column(db.Integer(), primary_key=True)
    course_name = db.Column(db.String(50), nullable=False, unique=True)
    Tutor = db.Column(db.String(), nullable=False)
    credit_hours = db.Column(db.Integer(), default=1)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'))
    students = db.relationship('Student', secondary='student_course', backref=db.backref('courses', lazy='dynamic'))
    
    def __repr__(self):
        return f"<Course {self.id}>"
            
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()



