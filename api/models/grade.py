from ..utils import db 

class Grade(db.Model):
    __tablename__= "grades"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    score = db.Column(db.Float , nullable=False)
    grade = db.Column(db.String(10) , nullable=True )

    def __repr__(self):
        return f"<Grade {self.id}>"
            
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()





