from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setting  the secret key for the session
app.config['SECRET_KEY'] = '22211788'

# Configuring  the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Defining  the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer)

# I am creating  the database tables
with app.app_context():
    db.create_all()

# IrRoute to display the list of books
@app.route('/books')
def books():
    book_list = Book.query.all()
    return render_template('books.html', books=book_list)

#I gain route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get book details from the form
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']

        # I am creating a new book instance
        new_book = Book(title=title, author=author, publication_year=publication_year)

        # Adding  the book to the database
        db.session.add(new_book)
        db.session.commit()

        # Redirecting  to the list of books
        return redirect(url_for('books'))

    return render_template('add_book.html')

# Closing the database connection after each request
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run(debug=True)
