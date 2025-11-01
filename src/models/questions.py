from src.core.db import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    responses = db.relationship('Response', backref='question', lazy=True)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', back_populates='questions')

    def __repr__(self):
        return f"Question(id={self.id} text={self.text!r})"

class Statistic(db.Model):
    __tablename__ = 'statistics'

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Statistic for Question %r: %r agree, %r disagree>' % (
            self.question_id, self.agree_count, self.disagree_count
        )