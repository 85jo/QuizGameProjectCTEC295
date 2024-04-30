from myproject import app, db
from flask import render_template,redirect,request,url_for,flash,session,json
from flask_login import login_user,login_required,logout_user
from myproject.models import User, Item
import requests
import pprint
from sqlalchemy import desc

from myproject.forms import LoginForm,RegistrationForm,ItemForm,BidForm
import datetime 


##Home Page
@app.route('/')
def home():
    
    url = f"https://opentdb.com/api.php?amount=1"

    # Sending a  GET request to the API and parse the JSON response
    response = requests.get(url)
    #Extracting JSON data
    #data = response.json()
    
    questions = json.loads(response.text)
    pprint.pprint(questions)

    # Extracting and returning the results from the response, or an empty list if there are no results
    #return data.get('results', [])"
    return render_template('home.html', questions=questions)


##Profile Route gives you all your items you bid on and all Users if your an admin.
##Admin check is done in the Profile.html file
@app.route('/Leaderboard')
@login_required
def Leaderboard():
    users = User.query.order_by(desc(User.score)).all()
    return render_template('Leaderboard.html',users=users)

@app.route('/Profile')
@login_required
def Profile():
    users = User.query.order_by(desc(User.score)).all()
    return render_template('Profile.html',users=users)

@app.route('/Quiz')
@login_required
def Quiz():
    users = User.query.all()
    return render_template('QuizPage.html',users=users)

@app.route('/Admin')
@login_required
def Admin():
    users = User.query.all()
    return render_template('Admin.html',users=users)

@app.route('/updateScore', methods=['POST'])
@login_required
def updateScore():
    data = request.get_json()
    newScore = data['score']
    user = User.query.filter_by(id = session['id']).first()
    user.score += int(newScore)
    db.session.commit()
    return render_template('Profile.html', user=user)

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
                    is_admin= form.is_admin.data,
                    score=0)
        
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


if __name__== '__main__':
    app.run(debug=True)

