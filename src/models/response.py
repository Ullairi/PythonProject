from src.core.db import db


class Response(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    is_agree = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        status = "Agree" if self.is_agree else "Disagree"
        return f"<Response id={self.id} question_id={self.question_id} status={status}>"