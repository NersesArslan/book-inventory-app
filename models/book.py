
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    books = db.relationship('Book', backref='genre',
                            cascade="all, delete-orphan", lazy=True)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey(
        'genres.id'), nullable=False)
    stock = db.Column(db.Integer, default=1)
