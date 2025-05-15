
from models.book import db, Book
from flask import Flask, render_template, request, flash, redirect, url_for
from models.book import Genre
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///app.db'
)

db.init_app(app)

app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    genres = Genre.query.paginate(page=page, per_page=10)
    return render_template('home.html', genres=genres)


@app.route('/genre/<genre_name>')
def view_genre(genre_name):
    genre_name = genre_name.replace('-', ' ')
    genre = Genre.query.filter_by(name=genre_name).first_or_404()
    books = Book.query.filter_by(genre_id=genre.id).all()
    return render_template('genre_books.html', genre=genre, books=books)


@app.route('/genre/add', methods=['POST'])
def add_genre():
    name = request.form['name'].strip()
    if name:
        new_genre = Genre(name=name)
        db.session.add(new_genre)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/genre/<int:genre_id>/add_book', methods=['POST'])
def add_book_to_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    title = request.form['title'].strip()
    author = request.form['author'].strip()
    stock_str = request.form.get('stock', '').strip()
    # Server-side validation for stock
    try:
        stock = int(stock_str)
        if stock < 1:
            raise ValueError
    except ValueError:
        flash('Stock must be a positive integer.', 'danger')
        return redirect(url_for('view_genre', genre_name=genre.name.replace(' ', '-')))
    existing_book = Book.query.filter_by(title=title, author=author).first()
    if existing_book:
        flash(
            f"A book with the title '{title}' by '{author}' already exists in another genre.", 'danger')
        return redirect(url_for('view_genre', genre_name=genre.name.replace(' ', '-')))
    new_book = Book(title=title, author=author, genre_id=genre.id, stock=stock)
    db.session.add(new_book)
    db.session.commit()
    flash(f"Book '{title}' by '{author}' added successfully!", 'success')
    return redirect(url_for('view_genre', genre_name=genre.name.replace(' ', '-')))


@app.route('/genre/<int:genre_id>/edit', methods=['GET', 'POST'])
def edit_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            flash('Genre name cannot be empty.', 'danger')
            return render_template('edit_genre.html', genre=genre)
        genre.name = name
        db.session.commit()
        flash('Genre updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_genre.html', genre=genre)


@app.route('/genre/<int:genre_id>/delete', methods=['POST'])
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    return redirect(url_for('index'))

# Book CRUD


@app.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title'].strip()
        book.author = request.form['author'].strip()
        book.stock = int(request.form['stock'].strip())
        db.session.commit()
        return redirect(url_for('view_genre', genre_name=book.genre.name.replace(' ', '-')))
    return render_template('edit_book.html', book=book)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    genre_name = book.genre.name.replace(' ', '-')
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('view_genre', genre_name=genre_name))


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    books = Book.query.filter(Book.title.ilike(
        f'%{query}%') | Book.author.ilike(f'%{query}%')).all()
    return render_template('search_results.html', books=books, query=query)


if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')
