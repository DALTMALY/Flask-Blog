#module for actual date
from datetime import datetime
#itsdangerous is a flask package with which we can generate a secure time-sensitive token for make sure that only someone who has access to the user's email can reset their password
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref='author', lazy = True)

    def get_reset_token(self, expires_sec = 1800):
        #We serializer "secret_key" of our token, "secret_key" is a environ variable, and expires_sec is the time token will be able
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod #tells to python not to expect that self paremeter as an argument
    def verify_reset_token(token):
        #We serializer "secret_key" of our token, "secret_key" is a environ variable
        s = Serializer(app.config['SECRET_KEY'])
        #If there a token
        try:
            #We take our user_id and we adding in "token" parameter, method "loads" is for validate if it's about a valid token and save in user_id variable
            user_id = s.loads(token)['user_id']
        #If is not a valid token
        except:
            #The None keyword is used to define a null value
            return None
        #If we are able to get the user ID without throwing an exception then let's just return the user with that ID
        return User.query.get(user_id) #user_id is the variable that contains the token
    #this is how our object is printed whenever we print it out
    def __repr__(self):
        #print User Object, "f" is for concatenate
        return f"User('{self.username}', '{self.email}, {self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    content = db.Column(db.Text, nullable = False,)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    #this is how our object is printed whenever we print it out
    def __repr__(self):
        #print Post Object, "f" is for concatenate
        return f"Post('{self.title}', '{self.date_posted}')"