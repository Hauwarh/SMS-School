from ..utils import db


class StudentCourse(db.Model):
    __tablename__='studentcourse'
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.studentId'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))

    def __repr__(self):
        return f"<StudentCourse {self.id}>"
            
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()



