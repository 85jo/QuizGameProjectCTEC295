from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from app import Libraries,Books,db,libToBook

##in terminal or cmd flask shell, import fakeIt,fakeIt.books(),fakeIt.library(10),fakeIt.add(library_id)
##fakeIt.add(library_id) will set random number looped 10 times and link them to whatever library id you enter in parameter.
##run for however many library id's you have

def books():
        book1 = Books(bookName = "The Hunger Games", author = "Suzanne Collins")
        book2 = Books(bookName = "The Fault in Our Stars", author = "John Green")
        book3 = Books(bookName = "To Kill a Mockingbird", author = "Harper Lee")
        book4 = Books(bookName = "The Silent Patient ", author = "Alex Michaelides")
        book5 = Books(bookName = "Paper Towns",author = "Jon Green")
        book6 = Books(bookName = "Catching Fire",author = "karen Collins")
        book7 = Books(bookName = "Mockingjay",author = "beth Collins")
        book8 = Books(bookName = "Pride and Prejudice",author = "Jane Austen")
        book9 = Books(bookName = "The Host",author = "Stephanie Meyer")
        book10 = Books(bookName = "The Midnight Library",author = "Matt Haig")
        db.session.add_all([book1,book2,book3,book4,book5,book6,book7,book8,book9,book10])
        db.session.commit()

def library(count):
    fake = Faker()
    i = 0
    while i < count:
        library = Libraries(
            libName = fake.last_name()+" Public Library",
            address = fake.address())
        db.session.add(library)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def add(library_id):
    i = 0
    while i < 10:
        add = libToBook.insert().values(library_id = library_id, book_id = randint(1, 10))
        db.session.execute(add)   
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()