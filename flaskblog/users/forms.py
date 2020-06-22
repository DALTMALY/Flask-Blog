#WTForms is a flexible forms validation and rendering library for Python web development. It can work with whatever web framework and template engine you choose. It supports data validation, CSRF protection, internationalization (I18N), and more. There are various community libraries that provide closer integration with popular frameworks.

#Without any configuration, the FlaskForm will be a session secure form with csrf protection.
from flask_wtf import FlaskForm
#The FileField provided by Flask-WTF differs from the WTForms-provided field. It will check that the file is a non-empty instance of FileStorage, otherwise data will be None.

#Remember to set the enctype of the HTML form to multipart/form-data, otherwise request.files will be empty.
------------------------------------------------------------------------------------------------------------
#Flask-WTF supports validating file uploads with FileRequired and FileAllowed. They can be used with both Flask-WTF's and WTForms's FileField classes.
from flask_wtf.file import FileField, FileAllowed
#Fields are defined as members on a form in a declarative fashion:
from wtforms import StringField, PasswordField, SubmitField, BooleanField
#To validate the field, call its validate method, providing a form and any extra validators needed.

#DataRequired: Checks the field’s data is ‘truthy’ otherwise stops the validation chain.
#Length: Validates the length of a string.
#Email: Validates an email address. Requires email_validator package to be installed. For ex: pip install wtforms[email].
#EqualTo: Compares the values of two fields.
#ValidationError: Raised when a validator fails to validate its input
#InputRequired: Validates that input was provided for this field.
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,InputRequired
#for save if an user is logged
from flask_login import current_user
#We import the user model
from flaskblog.models import User

#To define a form, one makes a subclass of FlaskForm (Object importing from flask_wtf) and defines the fields declaratively as class attributes.
class RegistrationForm(FlaskForm):
    #Declarating fields and validations
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #Function that will validate if an username already exist
    def validate_username(self, username):
        #Using python interpreter for SQL sentences for look up the username in the database, saving them in one variable called user
        user = User.query.filter_by(username = username.data).first()
        if user:
            #if username exist inside the database then send a message in client side
            raise ValidationError('That username is taken. Please choose a new one.')
    #Function that will validate if an email already exist
    def validate_email(self, email):
        #Using python interpreter for SQL sentences for look up the email in the database, saving them in one variable called email
        email = User.query.filter_by(email = email.data).first()
        if email:
            #if email exist inside the database then send a message in client side
            raise ValidationError('That email is taken. Please choose a new one.')



class LoginForm(FlaskForm):
    email = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    #Function that will validate if an username already exist or the account which is trying to update is itself
    def validate_username(self, username):
        #If the account which is trying to update is not itself then access denied. Only the account itself can update data, not other.
        if username.data != current_user.username:
            #Using python interpreter for SQL sentences for look up the username in the database, saving them in one variable called user
            user = User.query.filter_by(username = username.data).first()
            if user:
                #if username exist inside the database then send a message in client side
                raise ValidationError('That username is taken. Please choose a new one.')

    #Function that will validate if an email already exist or the account which is trying to update is itself
    def validate_email(self, email):
        #If the account which is trying to update is not itself then access denied. Only the account itself can update data, not other.
        if email.data != current_user.email:
            #Using python interpreter for SQL sentences for look up the email in the database, saving them in one variable called email
            email = User.query.filter_by(email = email.data).first()
            if email:
                #if email exist inside the database then send a message in client side
                 raise ValidationError('That email is taken. Please choose a new one.')



class RequestResetForm(FlaskForm):
    email = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    submit = SubmitField('Request Password Reset')

    #Function that will validate if there are some email in the database and if It is the same email in the input for reset password
    def validate_email(self, email):
        #Using python interpreter for SQL sentences for look up the email in the database, saving them in one variable called email
        email = User.query.filter_by(email = email.data).first()
        #If email doesn't exist then:
        if email is None:
            #Send a message in the client side
            raise ValidationError('Any account with that email Register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')