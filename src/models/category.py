from src.core.db import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    questions = db.relationship('Question', back_populates='category', lazy=True)

    def __repr__(self):
        return f"<Category id={self.id} name={self.name!r}>"