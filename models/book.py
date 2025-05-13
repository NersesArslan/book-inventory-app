
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

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
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey(
        'genres.id'), nullable=False)
    stock = db.Column(db.Integer, default=1, nullable=False)

    # Add a unique constraint
    __table_args__ = (UniqueConstraint('title', 'author',
                      'genre_id', name='unique_book_per_genre'),)
