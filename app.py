
from models.book import db, Book
from flask import Flask, render_template, request, redirect, url_for
from models.book import Genre

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://nersesarslanian:somepassword@localhost:5432/book_inventory"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    genres = Genre.query.all()
    return render_template('home.html', genres=genres)


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


@app.route('/genre/<int:genre_id>')
def view_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    books = Book.query.filter_by(genre_id=genre.id).all()
    return render_template('genre_books.html', genre=genre, books=books)


@app.route('/genre/add', methods=['POST'])
def add_genre():
    name = request.form['name']
    if name:
        new_genre = Genre(name=name)
        db.session.add(new_genre)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/genre/<int:genre_id>/add_book', methods=['POST'])
def add_book_to_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    title = request.form['title']
    author = request.form['author']
    stock = int(request.form.get('stock', 1))

    new_book = Book(title=title, author=author, genre_id=genre.id, stock=stock)
    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('view_genre', genre_id=genre.id))


@app.route('/genre/<int:genre_id>/edit', methods=['GET', 'POST'])
def edit_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    if request.method == 'POST':
        genre.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_genre.html', genre=genre)


@app.route('/genre/<int:genre_id>/delete', methods=['POST'])
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    return redirect(url_for('index'))

# Book CRUD


@app.route('/book/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    genre_id = request.form['genre_id']
    stock = int(request.form.get('stock', 1))
    new_book = Book(title=title, author=author, genre_id=genre_id, stock=stock)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
