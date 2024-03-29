import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MysecretKey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

libToBook = db.Table('libToBook',
                     db.Column('library_id',db.Integer,db.ForeignKey('library.id')),
                     db.Column('book_id',db.Integer,db.ForeignKey('book.id')))

class Libraries(db.Model):

    __tablename__ = 'library'

    id = db.Column(db.Integer, primary_key = True)
    libName = db.Column(db.String(64), unique=True, index=True)
    address = db.Column(db.String(64),unique=True,index=True)
    book_id = db.relationship('Books', secondary=libToBook, backref = db.backref('library', lazy='dynamic'), lazy='dynamic')

    def __init__(self,libName,address):
        self.libName = libName
        self.address = address

class Books(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key = True)
    bookName = db.Column(db.String(64),index=True)
    author = db.Column(db.String(64),index=True)

    def __init__(self,bookName,author):
        self.bookName = bookName
        self.author = author

@app.route('/')
def home():
    libraries = Libraries.query.all()
    books = Books.query.all()
    return render_template('home.html',libraries=libraries,books=books)

@app.route('/books')
def books():
    books = Books.query.all()
    return render_template('books.html',books=books)

@app.route('/library')
def library():
    libraries = Libraries.query.all()
    return render_template('library.html',libraries=libraries)

@app.route('/booksToLib/<int:library_id>')
def booksToLib(library_id):
    library = Libraries.query.get_or_404(library_id)
    inBooks = Books.query.join(libToBook).join(Libraries).filter(Libraries.id == library_id).all()
    return render_template('booksToLib.html',inBooks=inBooks,library = library)

@app.route('/libraryToBook/<int:book_id>')
def libraryToBook(book_id):
    book = Books.query.get_or_404(book_id)
    inLibraries = Libraries.query.join(libToBook).join(Books).filter(Books.id == book_id).all()
    return render_template('libraryToBook.html',inLibraries=inLibraries,book=book)

if __name__== '__main__':
    app.run(debug=True)