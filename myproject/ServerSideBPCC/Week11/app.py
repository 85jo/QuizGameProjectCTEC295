import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template
from faker import Faker

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MysecretKey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


class Owner(db.Model):

    __tablename__ = 'owner'

    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(64), unique=True, index=True)
    lastName = db.Column(db.String(64),unique=True,index=True)
    prefix = db.Column(db.String(128))
    Ownercompany = db.relationship('Company',backref = 'owner', lazy='dynamic')

    def __init__(self,firstName,lastName,prefix):
        self.firstName = firstName
        self.lastName = lastName
        self.prefix = prefix

class Company(db.Model):

    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.String(64), unique=True, index=True)
    motto = db.Column(db.String(64),unique=True,index=True)
    owner_id = db.Column(db.Integer,db.ForeignKey('owner.id'))

    def __init__(self,company,motto,owner_id):
        self.company = company
        self.motto = motto
        self.owner_id = owner_id

@app.route('/')
def home():
    owner = Company.query.all()
    return render_template('home.html',owners=owner)

if __name__== '__main__':
    app.run(debug=True)