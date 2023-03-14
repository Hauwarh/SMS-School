from ..utils import db

class Course(db.Model):
    __tablename__= 'courses'
    id =  db.Column(db.Integer(), primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    Tutor = db.Column(db.String(), nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'))




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



