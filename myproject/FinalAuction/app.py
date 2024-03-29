from myproject import app, db
from flask import render_template,redirect,request,url_for,flash,session
from flask_login import login_user,login_required,logout_user
from myproject.models import User, Item
import requests

from myproject.forms import LoginForm,RegistrationForm,ItemForm,BidForm
import datetime 
##Home Page
@app.route('/')
def home():
    
    url = f"https://opentdb.com/api.php?amount=50"

    # Sending a  GET request to the API and parse the JSON response
    response = requests.get(url)
    #Extracting JSON data
    data = response.json()

    app.logger.info (data)
    # Extracting and returning the results from the response, or an empty list if there are no results
    #return data.get('results', [])"
    return render_template('home.html')


##Profile Route gives you all your items you bid on and all Users if your an admin.
##Admin check is done in the Profile.html file
@app.route('/Profile')
@login_required
def Profile():
    item = Item.query.filter_by(highestBidder = session['id'])
    users = User.query.all()
    ##questions = Questions.query.all()
    return render_template('Profile.html',items=item,users=users)

##Logout Route,logs user out and redirects them to home.html
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out!")
    return redirect(url_for('home'))

##Log in page,will have them log in and redirect them to whatever page there were trying to access
##if the were trying to access a page that needed authentication
@app.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect('login')
        else:
            session['id'] = user.id
        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Logged in Successfully!')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('Profile')

            return redirect(next)
        
    return render_template('login.html', form=form)

##Registration page, adds user to the database.Then redirects them to login.html
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    phoneNum=form.phoneNum.data,
                    contactInfo=form.contactInfo.data,
                    is_admin= form.is_admin.data)
        
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful!")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

## Password Reset page, only accessable as an admin. Which on the navbar there is a check for admin
## which will give access to link to this route. NavBar is in base.html file.
## This takes in a user id matches it up to user in database auto fills registration form with info except password and admin fields.
## Then on submit, deletes old user and re adds them with the same info and updated password and/or admin ability to database.
@app.route('/PasswordReset/<int:userId>', methods=['GET','POST'])
@login_required
def PasswordReset(userId):
    form = RegistrationForm()
    user = User.query.filter_by(id=userId).first()

    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        user = User(email=form.email.data,
                    password=form.password.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    phoneNum=form.phoneNum.data,
                    contactInfo=form.contactInfo.data,
                    is_admin= form.is_admin.data)
        
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful!")
        return redirect(url_for('Profile'))
    form.email.data=user.email
    form.firstname.data=user.firstname
    form.lastname.data=user.lastname
    form.phoneNum.data=user.phoneNum
    form.contactInfo.data=user.contactInfo
    
    return render_template('PasswordReset.html', form=form, user=user)

## Gives ability to register new Item to the database. Also like link is only available if your 
## an Admin, through the navbar in base.html. then redirects to ItemListing
@app.route('/ItemRegister', methods=['GET','POST'])
@login_required
def ItemRegister():
    form = ItemForm()

    if form.validate_on_submit():
        item = Item(Title=form.Title.data,
                    description=form.description.data,
                    Bid=form.Bid.data,
                    endTime=form.endTime.data)
        
        db.session.add(item)
        db.session.commit()
        flash("Item Added Successfully!")
        return redirect(url_for('ItemListing'))
    return render_template('ItemRegister.html', form=form)


## Item Listing page avaliable to only bidders and admins queries all items current and past auctions.
## Does a date check to see if the auction is past or is still current
@app.route('/ItemListing')
@login_required
def ItemListing():
    item = Item.query.all()
    highbidder = User.query.all()
    dateNow = datetime.datetime.now()
    
    return render_template('ItemListing.html',items=item,highbidder=highbidder,dateNow=dateNow)

## Item Page takes an Item id from the Item Database from the ItemListing.html page
## that user clicks on to bid on. Gives all the item details and current bid,highest bidder and ability
## to bid on the item. Also will show a message if the bid is not over current bid.
@app.route('/ItemID/<int:itemId>', methods=['GET','POST'])
@login_required
def ItemID(itemId):
    form = BidForm()
    item = Item.query.filter_by(id=itemId).first()
    highbidder = User.query.filter_by(id=item.highestBidder).first()
    message = ""
    
    if highbidder != None:
        highbidderFN = highbidder.firstname
    else:
        highbidderFN = "None"
    currentUser = session['id']

    if form.validate_on_submit():
        if (form.Bid.data) > item.Bid:
            item.highestBidder = session['id']
            item.Bid = form.Bid.data
            db.session.commit()
            highbidder = User.query.filter_by(id=item.highestBidder).first()
            highbidderFN = highbidder.firstname

        else:
            message = "Bid is not more than current bid!"

        return render_template('Item.html',items=item,currentUser=currentUser,form=form,highbidder=highbidderFN,message=message)
    return render_template('Item.html',items=item,currentUser=currentUser,form=form,highbidder=highbidderFN)

if __name__== '__main__':
    app.run(debug=True)

