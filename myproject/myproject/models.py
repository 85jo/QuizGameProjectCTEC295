from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


##The User Database model
class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    phoneNum = db.Column(db.String(64))
    contactInfo = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    score = db.Column(db.Integer)

    def __init__(self,email,firstname,lastname,phoneNum,contactInfo,password,is_admin,score):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phoneNum = phoneNum
        self.contactInfo = contactInfo
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.score = score

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)


##The Item database model
class Item(db.Model):

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.String(64))
    description = db.Column(db.String(64))
    itemImageURL = db.Column(db.String(64))
    Bid = db.Column(db.Float(precision=2))
    highestBidder = db.Column(db.Integer())
    endTime = db.Column(db.DateTime())

    def __init__(self,Title,description,Bid,endTime):
        self.Title = Title
        self.description = description
        self.Bid = Bid
        self.endTime = endTime
