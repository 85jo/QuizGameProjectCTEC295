from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField, TextAreaField, DecimalField, DateField, FloatField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

##All the forms for the website

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegistrationForm(FlaskForm):
    email =StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords need to match')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    firstname =StringField('First Name',validators=[DataRequired()])
    lastname =StringField('Last Name',validators=[DataRequired()])
    phoneNum =StringField('Phone Number',validators=[DataRequired()])
    contactInfo =TextAreaField('Contact Information',validators=[DataRequired()])
    is_admin = BooleanField('Is Admin')
    submit = SubmitField('Register!')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has already registered!')
        
    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists!')
        
class ItemForm(FlaskForm):
    Title =StringField('Title',validators=[DataRequired()])
    description = TextAreaField('Item Description',validators=[DataRequired()])
    itemImageUrl = StringField()
    Bid = DecimalField(places=2)
    endTime = DateField(format='%Y-%m-%d')
    submit = SubmitField('Add Item!')

class BidForm(FlaskForm):
    Bid = FloatField()
    submit = SubmitField('Place Bid!')