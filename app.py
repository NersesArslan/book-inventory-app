
from models.book import db, Book
from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://nersesarslanian:somepassword@localhost:5432/book_inventory"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    title = request.form.get('title')
    author = request.form.get('author')
    genre = request.form.get('genre')
    stock = request.form.get('stock', type=int)

    new_book = Book(title=title, author=author, genre=genre, stock=stock)
    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('entries_page'))


@app.route('/entries')
def entries_page():
    genres = db.session.query(Book.genre).distinct()
    books_by_genre = {genre[0]: Book.query.filter_by(
        genre=genre[0]).all() for genre in genres}
    return render_template('entries.html', books_by_genre=books_by_genre)


@app.route('/delete/<entry_id>', methods=['POST'])
def delete_entry(entry_id):
    global entries
    entries = [entry for entry in entries if entry['id'] != entry_id]
    return redirect(url_for('entries_page'))


if __name__ == '__main__':
    app.run(debug=True)
